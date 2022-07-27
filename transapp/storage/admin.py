from django.contrib import admin

from .models import Warehouse, Action, OpenningTime, Timespan


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    # 'openning_time',  'action_time'] #'workers']
    list_display = ['pk', '__str__']


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']  # 'time_delta', 'warehouse']


@admin.register(OpenningTime)
class OpenningTimeAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]


@admin.register(Timespan)
class TimespanAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']
