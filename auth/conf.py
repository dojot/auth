# This file contains the default configuration values
# and confiuration retrivement functions

import os

# database related configuration
try:
    dbName = os.environ['DB_NAME']
except KeyError:
    dbName = "postgres"

try:
    dbUser = os.environ['DB_USER']
except KeyError:
    dbUser = "auth"

try:
    dbPdw = os.environ['DB_PWD']
except KeyError:
    dbPdw = ""

try:
    dbHost = os.environ['DB_HOST']
except KeyError:
    dbHost = "http://postgres"


# kong related configuration
try:
    kongURL = os.environ['KONG_URL']
except KeyError:
    kongURL = "http://kong:8001"

# JWT token related configuration
try:
    tokenExpiration = int(os.environ['TOKEN_EXP'])
except KeyError:
    tokenExpiration = 420
