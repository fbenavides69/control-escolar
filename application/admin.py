'''
'''
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db
from .models import User
from .models import Role
from .models import RolesUsers

admin = Admin()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(RolesUsers, db.session))
