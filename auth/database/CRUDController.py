#this file contains function to create, update and delete Users, groups and permission
import sqlalchemy
import re
from database.Models import Permission, User, Group, PermissionEnum

class NotFound(Exception):
    def __init__(self, message):
        self.message = message

#helper function to check user fields
def checkUser(user, ignore = []):
    if 'username' not in user.keys() or len(user['username']) == 0:
        raise ValueError('Missing username')

    if re.match(r'^[a-z0-9_]+$', user['username']) is None:
        raise ValueError('Invalid username, only lowercase alhpanumeric and underscores allowed')

    if ('passwd' not in ignore) and ('passwd' not in user.keys() or len(user['passwd']) == 0):
        raise ValueError('Missing passwd')

    if 'service' not in user.keys() or len(user['service']) == 0:
        raise ValueError('Missing service')
    if re.match(r'^[a-z0-9_]+$', user['username']) is None:
        raise ValueError('Invalid username, only alhpanumeric and underscores allowed')

    if 'email' not in user.keys() or len(user['email']) == 0:
        raise ValueError('Missing email')
    if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', user['email']) is None:
        raise ValueError('Invalid email address')

    if 'name' not in user.keys() or len(user['name']) == 0:
        raise ValueError("Missing user's name (full name)")

    return user

#user CRUD
def createUser(dbSession, user):
    checkUser(user)
    try:
        anotherUser =  dbSession.query(User.id).filter_by(username=user['username']).one()
        raise ValueError("username '" + user['username'] + "' is in use.")
    except sqlalchemy.orm.exc.NoResultFound:
        pass
    try:
        anotherUser =  dbSession.query(User.id).filter_by(email=user['email']).one()
        raise ValueError("Email '" + user['email'] + "' is in use.")
    except sqlalchemy.orm.exc.NoResultFound:
        pass
    user = User(**user)
    dbSession.add(user)
    return user

def searchUser(dbSession, username = None):
    userQuery = dbSession.query(User)

    if (username is not None and len(username) > 0):
        userQuery = userQuery.filter(User.username.like('%' + username + '%'))

    users = userQuery.all()
    if (len(users) == 0):
        raise NotFound("No results found with these filters")
    return users

def getUser(dbSession, userId):
    try:
        user = dbSession.query(User).filter_by(id=userId).one()
        return user
    except sqlalchemy.orm.exc.NoResultFound:
        raise NotFound("No user found with this ID")

def updateUser(dbSession, userId, userData):
    checkUser(userData)
    updated = dbSession.query(User).filter_by(id=userId) \
            .update(userData)
    if (updated == 0):
        raise NotFound("No user found with this ID")

def deleteUser(dbSession, userId):
    try:
        user = dbSession.query(User).filter_by(id=userId).one()
        dbSession.delete(user)
    except sqlalchemy.orm.exc.NoResultFound:
        raise NotFound("No user found with this ID")

#helper function to check permission fields
def checkPerm(perm):
    if 'permission' in perm.keys():
        if (perm['permission'] not in [p.value for p in PermissionEnum]):
            raise ValueError("An access control rule can not return '" + perm['permission'] + "'")
    else:
        #default value
        perm['permission'] = 'permit'

    if 'path' not in perm.keys() or len(perm['path']) == 0:
        raise ValueError('Missing permission Path')

    if 'method' not in perm.keys() or len(perm['method']) == 0:
        raise ValueError('Missing permission method')
    #TODO: check if path and method are valid regex

#creae a permission
def createPerm(dbSession, permission):
    checkPerm(permission)
    perm = Permission(**permission)
    dbSession.add(perm)
    return perm

def searchPerm(dbSession, path=None, method=None, permission=None):
    permQuery = dbSession.query(Permission)
    if (path is not None and len(path) > 0):
        permQuery = permQuery.filter(Permission.path.like('%' + path + '%'))
    if (method is not None and len(method) > 0):
        permQuery = permQuery.filter(Permission.method.like('%' + method + '%'))
    if (permission is not None and len(permission) > 0):
        if (permission not in [p.value for p in PermissionEnum]):
            raise ValueError("Invalid filter. Permission can't be '" + permission + "'")
        permQuery = permQuery.filter_by(permission=permission)

    perms = permQuery.all()
    if (len(perms) == 0):
        raise NotFound("No results found with these filters")
    return perms

def getPerm(dbSession, permissionId):
    try:
        perm = dbSession.query(Permission).filter_by(id=permissionId).one()
        return perm
    except sqlalchemy.orm.exc.NoResultFound:
        raise NotFound("No permission found with this ID")

def updatePerm(dbSession, permissionId, permData):
    checkPerm(permData)
    updated = dbSession.query(Permission).filter_by(id=permissionId) \
            .update(permData)
    if (updated == 0):
        raise NotFound("No permission found with this ID")

def deletePerm(dbSession, permissionId):
    try:
        perm = dbSession.query(Permission).filter_by(id=permissionId).one()
        dbSession.delete(perm)
    except sqlalchemy.orm.exc.NoResultFound:
        raise NotFound("No permission found with this ID")

def checkGroup(group):
    if 'name' not in group.keys() or len(group['name']) == 0:
        raise ValueError('Missing group name')
    if re.match(r'^[a-zA-Z0-9]+$', group['name']) is None:
        raise ValueError('Invalid group name, only alhpanumeric allowed')

    #TODO: must chekc the description?

def createGroup(dbSession, group):
    checkGroup(group)
    try:
        anotherGroup =  dbSession.query(Group.id).filter_by(name=group['name']).one()
        raise ValueError("Group name '" + group['name'] + "' is in use.")
    except sqlalchemy.orm.exc.NoResultFound:
        pass
    g = Group(**group)
    dbSession.add(g)
    return g

def searchGroup(dbSession, name=None):
    groupQuery = dbSession.query(Group)
    if (name is not None and len(name) > 0):
        groupQuery = groupQuery.filter(Group.name.like('%' + name + '%'))

    groups = groupQuery.all()
    if (len(groups) == 0):
        raise NotFound("No results found with these filters")

    return groups

def getGroup(dbSession, groupId):
    try:
        group = dbSession.query(Group).filter_by(id=groupId).one()
        return group
    except sqlalchemy.orm.exc.NoResultFound:
        raise NotFound("No group found with this ID")

def updateGroup(dbSession, groupId, groupData):
    checkUser(groupData)
    updated = dbSession.query(Group).filter_by(id=groupId) \
            .update(groupData)
    if (updated == 0):
        raise NotFound("No group found with this ID")

def deleteGroup(dbSession, groupId):
    try:
        group = dbSession.query(Group).filter_by(id=groupId).one()
        dbSession.delete(group)
    except sqlalchemy.orm.exc.NoResultFound:
        raise NotFound("No group found with this ID")
