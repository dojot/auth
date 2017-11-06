# This file contains the default configuration values
# and confiuration retrivement functions

import os


# database related configuration
dbName = os.environ.get("AUTH_DB_NAME", "postgres")
dbUser = os.environ.get("AUTH_DB_USER", "auth")
dbPdw = os.environ.get("AUTH_DB_PWD", "")
dbHost = os.environ.get("AUTH_DB_HOST", "postgres")


# cache related configuration
cacheName = os.environ.get("AUTH_CACHE_NAME", "redis")
cacheUser = os.environ.get("AUTH_CACHE_USER", "redis")
cachePdw = os.environ.get("AUTH_CACHE_PWD", "")
cacheHost = os.environ.get("AUTH_CACHE_HOST", "redis")
cacheTtl = int(os.environ.get("AUTH_CACHE_TTL", 720))
cacheDatabase = os.environ.get("AUTH_CACHE_DATABASE", "0")

# kong related configuration
kongURL = os.environ.get("AUTH_KONG_URL", "http://kong:8001")


# JWT token related configuration
tokenExpiration = int(os.environ.get("AUTH_TOKEN_EXP", 420))

# if auth should verify JWT signatures. Ative this will cause one
# query of overhead.
checkJWTSign = (os.environ.get("AUTH_TOKEN_CHECK_SIGN", "FALSE") in
                ['true', 'True', 'TRUE'])

# email related configuration
emailHost = os.environ.get("AUTH_EMAIL_HOST", "")
emailPort = int(os.environ.get("AUTH_EMAIL_PORT", 587))
emailUsername = os.environ.get("AUTH_EMAIL_USER", "")
emailPasswd = os.environ.get("AUTH_EMAIL_PASSWD", "")

# passwd policies configuration
passwdRequestExpiration = int(os.environ.get("AUTH_PASSWD_REQUEST_EXP", 30))
passwdHistoryLen = int(os.environ.get("AUTH_PASSWD_HISTORY_LEN", 4))
