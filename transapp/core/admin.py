from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages"""
    list_display = [ 'pk', 'username', 'email', 'workplace', 'position', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'workplace', 'position', 'email', 'password')}),
    )

admin.site.register(models.User, UserAdmin)


