from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from document.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']
