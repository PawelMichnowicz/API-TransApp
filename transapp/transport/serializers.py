"""
Serializers for transport APIs
"""
from rest_framework import serializers
from .models import Route, Transport, Vehicle, Order

class VehicleSerializer(serializers.ModelSerializer):
    ''' Serializer for vehcile views '''
    class Meta:
        model = Vehicle
        fields = ['pk', 'registration', 'capacity', 'is_available', 'is_refrigerate']


class RouteSerializer(serializers.ModelSerializer):
    ''' Serializer for route views '''
    class Meta:
        model = Route
        fields = ['pk', 'origin', 'destination']


class TransportSerializer(serializers.ModelSerializer):
    ''' Serializer for transport views '''
    class Meta:
        model = Transport
        fields = ['route', 'need_refrigerate', 'orders']

class OrderSerializer(serializers.ModelSerializer):
    ''' Serializer for order views '''
    class Meta:
        model = Order
        fields = ['buyer_email', 'price']