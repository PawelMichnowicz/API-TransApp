from django.contrib import admin

from .models import Vehicle, Route, Transport, Order


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'registration',
                    'capacity', 'is_available', 'is_refrigerate']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'buyer_email',  'transport', 'price', 'products']#'id_order',


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'origin', 'destination']


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ['pk', 'route', 'vehicle', 'need_refrigerate', 'action']
