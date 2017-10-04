from flask import Flask
from flask import make_response as fmake_response
import json
from flask_sqlalchemy import SQLAlchemy

import database.dbconf as dbconf

#make the initial flask + alchem configuration
app = Flask(__name__)
app.url_map.strict_slashes = False

#select database driver
if (dbconf.dbName == 'postgres'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+pypostgresql://' + \
                    dbconf.dbUser + ':' + dbconf.dbPdw + '@' + dbconf.dbHost

else:
    print("Currently, there is no suport for database " + dbconf.dbName)
    exit(-1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.create_all()

#utility function for HTTP responses
def make_response(payload, status):
    resp = fmake_response(payload, status)
    resp.headers['content-type'] = 'application/json'
    return resp

def formatResponse(status, message=None):
    payload = None
    if message:
        payload = json.dumps({ 'message': message, 'status': status})
    elif status >= 200 and status < 300:
        payload = json.dumps({ 'message': 'ok', 'status': status})
    else:
        payload = json.dumps({ 'message': 'Request failed', 'status': status})
    return make_response(payload, status);

def loadJsonFromRequest(request):
    if request.mimetype != 'application/json':
        raise ValueError('invalid mimetype')

    return request.get_json()
