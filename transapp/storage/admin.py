from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Warehouse, Action, OpenningTime, ActionWindow


class WorkersInline(admin.StackedInline):
    model = get_user_model()
    fields = ['username', 'position']
    raw_id_fields = ['workplace', ]
    max_num = 0


class ActionsInline(admin.StackedInline):
    model = Action
    fields = ['action_type', 'status']
    raw_id_fields = ['warehouse', ]
    max_num = 0

class ActionWindowInLine(admin.StackedInline):
    model = ActionWindow
    fields = ['monthday', 'from_hour', 'to_hour']
    raw_id_fields = ['warehouse', ]
    max_num = 0

class OpenningTimeInLine(admin.StackedInline):
    model = OpenningTime
    fields = ['weekday', 'from_hour', 'to_hour']
    raw_id_fields = ['warehouse', ]
    max_num = 0


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']
    inlines = [WorkersInline, ActionsInline, ActionWindowInLine, OpenningTimeInLine]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']


@admin.register(OpenningTime)
class OpenningTimeAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]


@admin.register(ActionWindow)
class ActionWindownAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']
