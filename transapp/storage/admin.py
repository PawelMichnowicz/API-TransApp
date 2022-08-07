from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Warehouse, Action, OpenningTime, Timespan

# class WorkersInline(admin.StackedInline):
#     model = get_user_model()
#     fields = ['username', 'position']
#     extra = 0

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']
# inlines = [WorkersInline, ]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']


@admin.register(OpenningTime)
class OpenningTimeAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]


@admin.register(Timespan)
class TimespanAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']
