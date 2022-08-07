from rest_framework import serializers
from .models import Route, Transport, Vehicle, Order


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['pk', 'registration', 'capacity', 'is_available', 'is_refrigerate']


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ['pk', 'origin', 'destination']


class TransportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transport
        fields = ['route', 'need_refrigerate', 'orders']

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['buyer', 'price', 'products']