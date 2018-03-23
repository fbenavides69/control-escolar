# -*- coding: utf-8 -*-

''' Flask SQL Alchemy ORM

    Define the Flask-Security database User and Roles schema
    to be used.be

    To create/recreate the database instance, from the python
    interactive shell (control-escolar):
        from application import create_app
        from application.models import db
        app = create_app()
        app.app_contect().push()
        db.create_all()
'''

from flask_security import RoleMixin
from flask_security import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

# Initialize the SQL Alchemy object
db = SQLAlchemy()


# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<name> {}'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer())
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = relationship(
        'Role',
        secondary=roles_users,
        backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<username> {} {}'.format(
            self.username, 'Active' if self.active else 'Non Active')
