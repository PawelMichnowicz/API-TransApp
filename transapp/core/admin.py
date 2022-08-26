"""
Django admin customization for user.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User

class UserAdmin(BaseUserAdmin):
    """Define the admin fields and options in admin panel"""
    list_display = [ 'pk', 'email', 'workplace', 'position', 'is_superuser']
    fieldsets = (
        (None, {'fields': ( 'workplace', 'position', 'email', 'password',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    ordering = ['id']

admin.site.register(User, UserAdmin)

