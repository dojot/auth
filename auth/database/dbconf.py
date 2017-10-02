#This file contain Database related configuration

import os

try:
    dbName = os.environ['DB_NAME']
except KeyError:
    dbName = "postgres"

try:
    dbUser = os.environ['DB_USER']
except KeyError:
    dbUser = "pyrbac"

try:
    dbPdw = os.environ['DB_PWD']
except KeyError:
    dbPdw = "pwd12"

try:
    dbHost = os.environ['DB_HOST']
except KeyError:
    dbHost = "localhost"
