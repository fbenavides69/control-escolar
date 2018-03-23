# -*- coding: utf-8 -*-

''' Flask Admin

    Define the administration views
'''

from flask_security import current_user
from flask_security import utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms.fields.simple import PasswordField
from .models import db
from .models import User
from .models import Role


class UserAdmin(ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a
    # User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available
    # Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has
    # the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field
    # corresponding to the model's password field. There are two reasons for
    # this. First, we want to encrypt the password before storing in the
    # database. Second, we want to use a password field (with the input
    # masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've
        # already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New
        # Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or
    # edited User -- before the changes are committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the
            # database. If the password field is blank, the existing password
            # in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(ModelView):

    # Prevent administration of Roles unless the currently logged-in user has
    # the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


admin = Admin()

admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))
