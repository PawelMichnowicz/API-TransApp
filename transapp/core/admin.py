from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from core.models import User, Document

class UserAdmin(BaseUserAdmin):
    """Define the admin pages"""
    list_display = [ 'pk', 'username', 'email', 'workplace', 'position', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'workplace', 'position', 'email', 'password',)}),
    )

admin.site.register(User, UserAdmin)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']
