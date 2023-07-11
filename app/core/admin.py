"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),   # optional
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)

# what is the orginial fieldsets?
# if i add a new user in the admin interface,
# will it call the create_user method in the UserManager and update to the database?

# !!!
# fieldsets sets up the fields that will be displayed on the form for editing
# an existing user in the admin site. The customized UserAdmin class in your
# example changes this to use the 'email', 'name', 'is_active', 'is_staff',
# 'is_superuser', and 'last_login' fields instead.

# When you register a model with the admin site (using admin.site.register(ModelName)),
# Django automatically sets up several views that you can use to interact with your model.

# When you create a new user through the Django admin site, Django uses the model's
# manager to create the user. The UserAdmin class uses the UserCreationForm to create
# new users, and UserCreationForm calls the create_user method on the model's default
# manager (i.e., User.objects.create_user()).

# In the Django admin interface, when creating a new user, the create_user method that
# will be called is the one that belongs to the manager assigned to the objects attribute
# in your User model.