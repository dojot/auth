import re

from database.Models import Permission, User, Group, PermissionEnum
from flaskAlchemyInit import HTTPRequestError


# Helper function to check request fields
def checkRequest(pdpRequest):
    if 'method' not in pdpRequest.keys() or len(pdpRequest['method']) == 0:
        raise HTTPRequestError(400, "Missing method")

    if 'username' not in pdpRequest.keys() or len(pdpRequest['username']) == 0:
        raise HTTPRequestError(400, "Missing username")

    if 'path' not in pdpRequest.keys() or len(pdpRequest['path']) == 0:
        raise HTTPRequestError(400, "Missing path")


def pdpMain(dbSession, pdpRequest):
    checkRequest(pdpRequest)
    # TODO: Create a materialised view
    user = dbSession.query(User). \
        filter_by(username=pdpRequest['username']).one()
    # Get all permissions of this user
    permissions = user.permissions
    permissions += [perm
                    for group in user.groups
                    for perm in group.permissions]
    q = dbSession.query(User)
    print(q)

    return makeDecision(permissions, pdpRequest['method'], pdpRequest['path'])


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
