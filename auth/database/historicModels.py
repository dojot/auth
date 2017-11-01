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
historicFields = ['deletion_date']


class UserInactive(db.Model):
    __tablename__ = 'user_inactive'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    username = Column(String(50), nullable=False)
    service = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_date = Column(DateTime, nullable=False)
    deletion_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Kong and passwd related fields don't need to be registered on historic
    def createInactiveFromUser(user):
        userInactiveDict = {
                                c.name: getattr(user, c.name)
                                for c in UserInactive.__table__.columns
                                if c.name not in historicFields
                            }

        inactiveUser = UserInactive(**userInactiveDict)
        return inactiveUser


class PasswdInactive(db.Model):
    __tablename__ = 'user_inactive'

    user_id = Column(Integer, autoincrement=False)
    hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    deletion_date = Column(DateTime, default=datetime.datetime.utcnow)

    def createInactiveFromUser(user):
        pwdInactiveDict = {
                                c.name: getattr(user, c.name)
                                for c in UserInactive.__table__.columns
                                if c.name not in historicFields
                            }

        inactivePwd = PasswdInactive(**pwdInactiveDict)
        user.hash = None
        user.salt = None
        return inactivePwd
