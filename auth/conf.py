#this file contains the default configuration values
#and confiuration retrivement functions

import os

try:
    kongURL = os.environ['KONG_URL']
except KeyError:
    kongURL = 'http://localhost:8001' #'http://kong:8001'

try:
    tokenExpiration = int( os.environ['TOKEN_EXP'] )
except KeyError:
    tokenExpiration =  420
