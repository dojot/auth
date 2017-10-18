import re
import jwt
import sqlalchemy

from database.Models import Permission, User, Group, PermissionEnum
from flaskAlchemyInit import HTTPRequestError


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
        raise HTTPRequestError(400, "Corrupted JWT")

    # TODO: Create a materialised view (or two)

    try:
        user = dbSession.query(User). \
                filter_by(id=jwtPayload['userid']).one()
    except (sqlalchemy.orm.exc.NoResultFound, KeyError):
        raise HTTPRequestError(400, "Invalid JWT payload")

    # now that we know the user, we know the secret
    # and can check the jwt signature
    try:
        options = {
            'verify_exp': False,
        }
        jwt.decode(pdpRequest['jwt'],
                   user.secret, algorithm='HS256', options=options)
    except jwt.exceptions.DecodeError:
        raise HTTPRequestError(400, "Invalid JWT signaure")

    # Get all permissions of this user
    permissions = user.permissions
    permissions += [perm
                    for group in user.groups
                    for perm in group.permissions]

    return makeDecision(permissions,
                        pdpRequest['action'],
                        pdpRequest['resource'])


# Receive a list of permissions and try to match the Given
# path + method with one. Return 'deny' or 'permit'
def makeDecision(permissionList, method, path):
    for p in permissionList:
        # if the Path and method Match
        if re.match(r'(^' + p.path + ')', path) is not None:
            # This case is so common that worth the separate if
            # TODO: return first match is OK?
            if p.method == '*':
                return p.permission.value
            if re.match(r'(^' + p.method + ')', method):
                return p.permission.value
    return 'deny'
