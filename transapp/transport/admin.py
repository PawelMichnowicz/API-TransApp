from django.contrib import admin

from .models import Vehicle, Route, Offer

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'registration', 'capacity', 'is_available', 'is_refrigerate']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['pk','origin', 'destination']

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['pk','id_offer','route', 'vehicle', 'need_refrigerate', 'accepted']








