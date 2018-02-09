from flask_security import RoleMixin
from flask_security import UserMixin
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RolesUsers(Base):
    __tablename__ = 'roles_users'

    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

    def __repr__(self):
        return '<RoleUser> {}'.format(self.user_id, self.role_id)


class Role(Base, RoleMixin):
    __tablename__ = 'role'

    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return '<name> {}'.format(self.name)


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer())
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship(
        'Role',
        secondary='roles_users',
        backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<username> {} {}'.format(
            self.username, 'Active' if self.active else 'Non Active')
