# Redis cache configuration
# powered by flask-redis: https://github.com/underyx/flask-redis
import conf
from .flaskAlchemyInit import app, db

if (conf.cacheName == 'redis'):
    from flask_redis import FlaskRedis
    REDIS_URL = ('redis://' + conf.cacheUser + ':' + conf.cachePdw
                 + '@localhost:6379/0' + conf.cacheHost)
    redis_store = FlaskRedis(app, strict=False,
                             charset="utf-8", decode_responses=True)

elif (conf.cacheName == 'NOCACHE'):
    print("Warning. Cache policy set to NOCACHE."
          "This may degrade PDP perfomance.")
    redis_store = None

else:
    print("Currently, there is no suport for cache policy " + conf.dbName)
    exit(-1)


# create a cache key
def generateKey(userid, action, resource):
    # add a prefix to every key, to avoid colision with others aplications
    key = 'PDP;'
    key += str(userid) + ';' + action + ';' + resource
    return key


# invalidate a key. may use regex patterns
def deleteKey(userid='*', action='*', resource='*'):
    if redis_store:
        # RE and Redis use diferent wildcard representations
        action = action.replace('(.*)', '*')
        resource = resource.replace('(.*)', '*')
        # TODO: put the cache update on a worker threaded
        key = generateKey(userid, action, resource)
        for dkey in redis_store.scan_iter(key):
            redis_store.delete(dkey)
