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
emailHost = os.environ.get("AUTH_EMAIL_HOST", "NOEMAIL")
emailPort = int(os.environ.get("AUTH_EMAIL_PORT", 587))
emailTLS = (os.environ.get("AUTH_EMAIL_TLS", "true") in
            ['true', 'True', 'TRUE'])
emailUsername = os.environ.get("AUTH_EMAIL_USER", "")
emailPasswd = os.environ.get("AUTH_EMAIL_PASSWD", "")

# passwd policies configuration
# time to expire an password reset link in minutes
passwdRequestExpiration = int(os.environ.get("AUTH_PASSWD_REQUEST_EXP", 30))
# how many passwords should be check on the user history
# to enforce no password repetition policy
passwdHistoryLen = int(os.environ.get("AUTH_PASSWD_HISTORY_LEN", 4))


# make some configuration checks
# and warn if dangerous configuration is found
if (emailHost == 'NOEMAIL'):
    print("MAIL_HOST set to NOEMAIL. This is unsafe"
          " and there's no way to reset users forgotten password")

if (emailHost != 'NOEMAIL' and
   (len(emailUsername) == 0 or len(emailPasswd) == 0)):
    print('Invalid configuration: No EMAIL_USER or EMAIL_PASSWD defined'
          ' although a EMAIL_HOST was defined')

if (emailHost != 'NOEMAIL' and not emailTLS):
    print('Using e-mail without TLS is not safe')

if (kongURL == 'DISABLED' and not checkJWTSign):
    print('Disabling KONG_URL and TOKEN_CHECK_SIGN is dangerous, as'
          ' auth have no way to guarantee a JWT token is valid')
