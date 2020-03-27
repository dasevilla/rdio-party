import logging
import time
import traceback
from datetime import datetime, timedelta

import spotipy
from django.conf import settings
from django.core.management.base import BaseCommand
from redis import ConnectionPool, StrictRedis

from sutrofm.redis_models import Party, Message

redis_connection_pool = ConnectionPool(**settings.WS4REDIS_CONNECTION)
logger = logging.getLogger(__name__)

WAIT_FOR_USERS = timedelta(minutes=5)


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('room_id', type=str)

  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self.redis = None
    self.party = None
    self.party_id = None
    self.currently_playing = None
    self.current_track_duration = None
    self.current_start_time = None
    self.keep_running = True

  def handle(self, room_id, *args, **kwargs):
    self.party_id = room_id
    self.redis = StrictRedis(connection_pool=redis_connection_pool)
    self.party = Party.get(self.redis, room_id)

    self.currently_playing = None
    self.current_track_duration = None
    self.current_start_time = None

    self.play_track(self.party.playing_track_key)

    self.run()

  def run(self):
    logger.debug('Starting up master process for party "%s"!', self.party_id)
    while self.keep_running:
      try:
        self.keep_running = self.tick()
      except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        logger.exception("!!! ALERT !!! Master... More like Crashster.")
      time.sleep(1)
    else:
      logger.debug('Nobody in room %s, killing' % self.party_id)

  def get_duration(self, track_key):
    client_credentials_manager = spotipy.SpotifyClientCredentials(client_id=settings.SOCIAL_AUTH_SPOTIFY_KEY,
                                                                  client_secret=settings.SOCIAL_AUTH_SPOTIFY_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    track = sp.track(track_key)
    logger.info(track)
    return track['duration_ms']

  def play_track(self, track_key):
    self.current_track_duration = None
    self.current_start_time = None
    self.currently_playing = None

    if track_key:
      self.currently_playing = track_key
      self.current_track_duration = self.get_duration(track_key)
      self.current_start_time = self.party.playing_track_start_time

  def play_next_track(self):
    # Refresh party data
    self.party.play_next_track()
    self.party.save(self.redis)

    was_playing = self.currently_playing
    self.play_track(self.party.playing_track_key)
    if was_playing != self.currently_playing:
      self.send_play_track_message(self.currently_playing)
    self.party.broadcast_player_state(self.redis)
    self.party.broadcast_queue_state(self.redis)

  def send_play_track_message(self, rdio_track_key):
    message = Message.make_now_playing_message(self.redis, self.party, rdio_track_key)
    message.save(self.redis)
    self.party.broadcast_message_added(self.redis, message)

  def tick(self):
    # Refresh the party data
    self.party = Party.get(self.redis, self.party_id)

    position = (datetime.utcnow() - (self.current_start_time or datetime.utcnow())).seconds
    if (not self.currently_playing) or (position > self.current_track_duration) or self.party.should_skip():
      self.play_next_track()

    self.party.broadcast_user_list_state(self.redis)
    return self.should_keep_running()

  def should_keep_running(self):
    """ Kill if no one is online in the room any more """
    return len(self.party.active_users())
