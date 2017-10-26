# Redis cache configuration
# powered by flask-redis: https://github.com/underyx/flask-redis
import conf
from .flaskAlchemyInit import app, db
from flask_redis import FlaskRedis

# redis.exceptions.ConnectionError

if (conf.cacheName == 'redis'):
    REDIS_URL = ('redis://' + conf.cacheUser + ':' + conf.cachePdw
                 + '@' + conf.cacheHost + ':6379/' + conf.cacheDatabase)
    app.config['DBA_URL'] = REDIS_URL
    redis_store = FlaskRedis(app, config_prefix='DBA', strict=False,
                             encoding="utf-8",
                             charset="utf-8", decode_responses=True)

# socket_keepalive socket_keepalive_options
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
