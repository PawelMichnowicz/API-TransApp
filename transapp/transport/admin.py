"""
Django admin customization for transport app.
"""
from django.contrib import admin

from .models import Vehicle, Route, Transport, Order

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    ''' Define admin panel for vehicle model '''
    list_display = ['pk', 'registration',
                    'capacity', 'is_available', 'is_refrigerate']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ''' Define admin panel for order model '''
    list_display = ['pk', 'buyer_email',  'transport', 'price']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    ''' Define admin panel for route model '''
    list_display = ['pk', 'origin', 'destination']


class OrdersInline(admin.StackedInline):
    ''' Inline using for display information about order model in warehouse admin panel '''
    model = Order
    raw_id_fields= ['transport',]
    fields = ['buyer_email',]
    readonly_fields = ['order_id' ]
    max_num=0

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    ''' Define admin panel for transport model '''
    list_display = ['pk', 'route', 'vehicle', 'need_refrigerate']
    inlines = [OrdersInline, ]