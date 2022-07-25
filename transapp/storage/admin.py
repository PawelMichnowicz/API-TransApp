from django.contrib import admin

from .models import Warehouse, ReceiveAction, SendAction, OpenningTime, Timespan, Timedelta

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__'] #'openning_time', 'receive_time', 'send_time'] #'workers']

@admin.register(ReceiveAction)
class ReceiveActionAdmin(admin.ModelAdmin):
    list_display = ['pk',] # 'time_delta', 'warehouse']

@admin.register(SendAction)
class SendActionAdmin(admin.ModelAdmin):
    list_display = ['pk',] # 'time_delta', 'warehouse']

@admin.register(OpenningTime)
class OpenningTimeAdmin(admin.ModelAdmin):
    list_display = ['__str__',]

@admin.register(Timespan)
class TimespanAdmin(admin.ModelAdmin):
    list_display = ['pk', ]

@admin.register(Timedelta)
class TimedeltaAdmin(admin.ModelAdmin):
    list_display = ['pk', ]

