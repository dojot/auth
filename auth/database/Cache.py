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
    redis_store = None

else:
    print("Currently, there is no suport for database " + dbconf.dbName)
    exit(-1)


# create a cache key
def generateKey(*args):
    # add a prefix to every key, to avoid colision with others aplications
    key = 'PDP'
    for w in args:
        key += ';' + str(w)
    return key
