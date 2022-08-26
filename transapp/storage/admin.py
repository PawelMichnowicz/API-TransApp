"""
Django admin customization for storage.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Warehouse, Action, OpenningTime, ActionWindow


class WorkersInline(admin.StackedInline):
    ''' Inline using for display information about workers in warehouse admin panel '''
    model = get_user_model()
    fields = ['position']
    raw_id_fields = ['workplace', ]
    max_num = 0


class ActionsInline(admin.StackedInline):
    ''' Inline using for display information about actions in warehouse admin panel '''
    model = Action
    fields = ['action_type', 'status']
    raw_id_fields = ['warehouse', ]
    max_num = 0

class ActionWindowInLine(admin.StackedInline):
    ''' Inline using for display information about action window in warehouse admin panel '''
    model = ActionWindow
    fields = ['monthday', 'from_hour', 'to_hour']
    raw_id_fields = ['warehouse', ]
    max_num = 0

class OpenningTimeInLine(admin.StackedInline):
    ''' Inline using for display information about openinng time in warehouse admin panel '''
    model = OpenningTime
    fields = ['weekday', 'from_hour', 'to_hour']
    raw_id_fields = ['warehouse', ]
    max_num = 0


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    ''' Define admin panel for warehouse model '''
    list_display = ['pk', '__str__']
    inlines = [WorkersInline, ActionsInline, ActionWindowInLine, OpenningTimeInLine]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    ''' Define admin panel for action model '''
    list_display = ['pk', '__str__']


@admin.register(OpenningTime)
class OpenningTimeAdmin(admin.ModelAdmin):
    ''' Define admin panel for openninng time model '''
    list_display = ['__str__', ]


@admin.register(ActionWindow)
class ActionWindownAdmin(admin.ModelAdmin):
    ''' Define admin panel for action window model '''
    list_display = ['pk', '__str__']
