import re
import jwt
import sqlalchemy

import conf
from database.Models import Permission, User, Group, PermissionEnum
from database.Models import MVUserPermission, MVGroupPermission
from database.flaskAlchemyInit import HTTPRequestError, app
import database.Cache as cache


# Helper function to check request fields
def checkRequest(pdpRequest):
    if 'action' not in pdpRequest.keys() or len(pdpRequest['action']) == 0:
        raise HTTPRequestError(400, "Missing action")

    if 'jwt' not in pdpRequest.keys() or len(pdpRequest['jwt']) == 0:
        raise HTTPRequestError(400, "Missing JWT")

    if 'resource' not in pdpRequest.keys() or len(pdpRequest['resource']) == 0:
        raise HTTPRequestError(400, "Missing resource")


def pdpMain(dbSession, pdpRequest):
    checkRequest(pdpRequest)
    try:
        jwtPayload = jwt.decode(pdpRequest['jwt'], verify=False)
    except jwt.exceptions.DecodeError:
        raise HTTPRequestError(401, "Corrupted JWT")

    try:
        user_id = jwtPayload['userid']
    except ():
        raise HTTPRequestError(401, "Invalid JWT payload")

    # now that we know the user, we know the secret
    # and can check the jwt signature
    if conf.checkJWTSign:
        try:
            user = dbSession.query(User). \
                    filter_by(user_id=jwtPayload['userid']).one()
            options = {
                'verify_exp': False,
            }
            jwt.decode(pdpRequest['jwt'],
                       user.secret, algorithm='HS256', options=options)
        except (jwt.exceptions.DecodeError, sqlalchemy.orm.exc.NoResultFound):
            raise HTTPRequestError(401, "Invalid JWT signaure")

    if cache.redis_store:
        cachedVeredict = cache.redis_store. \
                        get(cache.generateKey(user_id, pdpRequest['action'],
                                              pdpRequest['resource']))

        if cachedVeredict:
            return cachedVeredict

    veredict = iteratePermissions(user_id,
                                  jwtPayload['groups'],
                                  pdpRequest['action'],
                                  pdpRequest['resource'])
    # if Redis cache is ative, registry this veredict
    if cache.redis_store:
        cache.redis_store.setex(cache.generateKey(user_id,
                                                  pdpRequest['action'],
                                                  pdpRequest['resource']
                                                  ),
                                str(veredict),
                                30   # time to live
                                )
    return veredict


def iteratePermissions(user_id, groupsList, action, resource):
    permit = False

    # check user direct permissions
    for p in MVUserPermission.query.filter_by(user_id=user_id):
        granted = makeDecision(p, action, resource)
        # user permissions have precedence over group permissions
        if granted != PermissionEnum.notApplicable:
            return granted.value

    # check user group permissions
    for g in groupsList:
        for p in MVGroupPermission.query.filter_by(group_id=g):
            granted = makeDecision(p, action, resource)
            # deny have precedence over permits
            if granted == PermissionEnum.deny:
                return granted.value
            elif granted == PermissionEnum.permit:
                permit = True

    if permit:
        return PermissionEnum.permit.value
    else:
        return PermissionEnum.deny.value


# Receive a Permissions and try to match the Given
# path + method with it. Return 'permit' or 'deny' if succed matching.
# return 'notApplicable' otherwise
def makeDecision(permission, method, path):
    # if the Path and method Match
    if re.match(r'(^' + permission.path + ')', path) is not None:
        if re.match(r'(^' + permission.method + ')', method):
            return permission.permission
    return PermissionEnum.notApplicable
