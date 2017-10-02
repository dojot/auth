from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import conf

Base = declarative_base()

def initDatabase():
    dbDriver = None
    if (conf.dbName == 'postgres'):
        dbDriver = 'postgres+pypostgresql'

    if dbDriver is None:
        print("Currently, there is no suport for database " + conf.dbName)
        exit(-1)

    print(dbDriver + '://' + \
                    conf.dbUser + ':' + conf.dbPdw + '@' + conf.dbHost)

    try:
        engine = sqlalchemy.create_engine(dbDriver + '://' + \
                    conf.dbUser + ':' + conf.dbPdw + '@' + conf.dbHost)
    except:
        #TODO: find out what exception is throw
        print("Could not connect to the databse")
        exit(-1)

    # (sqlalchemy.exc.DBAPIError, sqlalchemy.util.queue.Empty, postgresql.exceptions.AuthenticationSpecificationError):
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    #create a databse session
    s = session()
    return s

#Model for the database tables
class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False)
    method = Column(String(30), nullable=False)
    permission = Column(String, nullable=False)
    users = relationship('User', secondary='user_permission',cascade="delete")
    groups = relationship('Group', secondary='group_permission',cascade="delete")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    permissions = relationship('Permission', secondary='user_permission', cascade="delete")
    groups = relationship('Group', secondary='user_group', cascade="delete")

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    #role = Column(Boolean)
    permissions = relationship('Permission', secondary='group_permission', cascade="delete")
    users = relationship('User', secondary='user_group', cascade="delete")

class UserPermission(Base):
    __tablename__ = 'user_permission'
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)

class GroupPermission(Base):
    __tablename__ = 'group_permission'
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True, index=True)

class UserGroup(Base):
    __tablename__ = 'user_group'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True, index=True)
