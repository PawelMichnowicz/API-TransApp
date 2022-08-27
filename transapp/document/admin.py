"""
Django admin customization for document
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from document.models import Document, Contractor


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    ''' Define admin panel for document model '''
    list_display = ['name', 'file']


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    ''' Define admin panel for contractor model '''
    list_display = [ 'nip', 'regon','nazwa']
