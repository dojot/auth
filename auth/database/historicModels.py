# This file contains models for inative users and passwords.
# These kind of information should not be hard removed
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
import datetime

import conf as dbconf
from .Models import User
from .flaskAlchemyInit import app, db

# a list of special fields present on all historic tables
# this list is necessary to avoid 'AttributeError' when coping from
# non-history objects
historicFields = ['inactive_id', 'deletion_date']


class UserInactive(db.Model):
    __tablename__ = 'user_inactive'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    username = Column(String(50), nullable=False)
    service = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_date = Column(DateTime, nullable=False)
    deletion_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Kong related fields don't need to be registered on historic
    # password related fields are stored on passwd_inactive table

    # receives a user model object and save it on inactive table
    def createInactiveFromUser(dbSession, user):
        userInactiveDict = {
                                c.name: getattr(user, c.name)
                                for c in UserInactive.__table__.columns
                                if c.name not in historicFields
                            }

        inactiveUser = UserInactive(**userInactiveDict)
        dbSession.add(inactiveUser)


class PasswdInactive(db.Model):
    __tablename__ = 'passwd_inactive'

    # sqlAlchemy require a primary key on every table
    inactive_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, autoincrement=False)
    hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    deletion_date = Column(DateTime, default=datetime.datetime.utcnow)

    # receives a user model object and save its passwd on inactive table
    def createInactiveFromUser(dbSession, user):
        if not user.hash:
            return
        pwdInactiveDict = {
                            'user_id': user.id,
                            'hash': user.hash,
                            'salt': user.salt
                           }

        inactivePwd = PasswdInactive(**pwdInactiveDict)
        dbSession.add(inactivePwd)


class PasswordRequestInactive(db.Model):
    __tablename__ = 'passwd_request_inactive'

    # sqlAlchemy require a primary key on every table
    inactive_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, autoincrement=False)
    link = Column(String, nullable=False, index=True)
    created_date = Column(DateTime, nullable=False)
    deletion_date = Column(DateTime, default=datetime.datetime.utcnow)

    # receives a PasswordRequest model object and
    # save its on the inactive table
    def createInactiveFromRequest(dbSession, pwdRequest):
        inactiveDict = {
                        c.name: getattr(pwdRequest, c.name)
                        for c in PasswordRequestInactive.__table__.columns
                        if c.name not in historicFields
                        }

        inactiveRequest = PasswordRequestInactive(**inactiveDict)
        dbSession.add(inactiveRequest)
