import simplejson

from django.conf import settings
from django.http import HttpResponse
from redis import ConnectionPool, StrictRedis

from sutrofm.redis_models import Party, User, Messages

redis_connection_pool = ConnectionPool(**settings.WS4REDIS_CONNECTION)


def parties(request):
    redis = StrictRedis(connection_pool=redis_connection_pool)
    parties = Party.getall(redis)
    data = [
        {
            "id": party.id,
            "name": party.name,
            "people": [
              {
                  "isOnline": False
              },
              {
                  "isOnline": True
              }
            ],
            "player": {
                "playingTrack": ({
                    "trackKey": party.playingTrackId
                } if party.playingTrackId else None)
            } 
        } for party in parties
    ]
    json_string = simplejson.dumps(data)
    return HttpResponse(json_string, content_type='text/json')

def users(request):
    redis = StrictRedis(connection_pool=redis_connection_pool)
    users = User.getall(redis)
    data = [
        {
            "id": user.id,
            "displayName": user.displayName,
            "iconUrl": user.iconUrl,
            "userUrl": user.userUrl,
            "rdioKey": user.rdioKey,
        } for user in users
    ]
    json_string = simplejson.dumps(data)
    return HttpResponse(json_string, content_type='text/json')

def get_user_by_id(request, user_id):
    redis = StrictRedis(connection_pool=redis_connection_pool)
    user = User.get(redis, user_id)
    data = {
        "id": user.id,
        "displayName": user.displayName,
        "iconUrl": user.iconUrl,
        "userUrl": user.userUrl,
        "rdioKey": user.rdioKey,
    }
    json_string = simplejson.dumps(data)
    return HttpResponse(json_string, content_type='text/json')

def messages(request, room_id):
    redis = StrictRedis(connection_pool=redis_connection_pool)
    messages = Messages.get_recent(redis, room_id)
    json_string = simplejson.dumps(messages)
    return HttpResponse(json_string, content_type='text/json')  



