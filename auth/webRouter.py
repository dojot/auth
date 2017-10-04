#!/usr/bin/python3
from flask import Flask
from flask import request
import json

import conf
import database.CRUDController as crud
import kongUtils as kong
from flaskAlchemyInit import app, db, formatResponse, make_response, loadJsonFromRequest

@app.route('/user', methods=['POST'])
def createUser():
    try:
        authData = loadJsonFromRequest(request)

        #create user
        newUser = crud.createUser(db.session, authData)

        #if no problems occur to create user (no exceptions), configure kong
        kongData = kong.configureKong(newUser.username)
        if kongData is None:
            return formatResponse(500, 'failed to configure verification subsystem')
        newUser.secret = kongData['secret']
        newUser.key = kongData['key']
        newUser.kongId = kongData['kongid']

        db.session.add(newUser)
        db.session.commit()
        return make_response(json.dumps({"user": newUser.safeDict(), "message": "user created"}), 200)
    except crud.BadRequest as err:
        return formatResponse(400, err.message )

@app.route('/user', methods=['GET'])
def listUsers():
    try:
        users = crud.searchUser(db.session, \
            #filters
            request.args['username'] if 'username' in request.args else None
        )
        usersSafe = list(map(lambda u: u.safeDict(), users))
        return make_response(json.dumps({ "users" : usersSafe}), 200)
    except crud.NotFound as nf:
        return formatResponse(404, nf.message)


@app.route('/user/<userid>', methods=['GET'])
def getUser(userid):
    try:
        user = crud.getUser(db.session, int(userid))
        return make_response(json.dumps({"user": user.safeDict()}), 200)
    except crud.NotFound as nf:
        return formatResponse(404, nf.message)

# should have restricted access
@app.route('/user/<userid>', methods=['PUT'])
def updateUser(userid):
    try:
        authData = loadJsonFromRequest(request)
        #update user fields
        oldUser = crud.updateUser(db.session, int(userid), authData)

        #create a new kong secret and delete the old one
        kongData = kong.configureKong(oldUser.username)
        if kongData is None:
            return formatResponse(500, 'failed to configure verification subsystem')

        kong.revokeKongSecret(oldUser.username, oldUser.kongId)
        oldUser.secret = kongData['secret']
        oldUser.key = kongData['key']
        oldUser.kongid = kongData['kongid']
        db.session.add(oldUser)
        db.session.commit()
        return formatResponse(200)

    except crud.NotFound as nf:
        return formatResponse(404, nf.message)
    except crud.BadRequest as err:
        return formatResponse(400, err.message )


@app.route('/user/<userid>', methods=['DELETE'])
def removeUser(userid):
    try:
        old_user = crud.getUser(db.session, int(userid))
        kong.removeFromKong(old_user.username)
        crud.deleteUser(db.session, int(userid))
        db.session.commit()
        return formatResponse(200, "User removed")
    except crud.NotFound as nf:
        return formatResponse(404, nf.message)
    except KongError as ke:
        return formatResponse(500,  ke.message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5003)
