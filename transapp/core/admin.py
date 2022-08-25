from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from core.models import User

class UserAdmin(BaseUserAdmin):
    """Define the admin pages"""
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

