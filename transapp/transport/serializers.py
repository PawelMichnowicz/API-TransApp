from rest_framework import serializers
from .models import Route, Offer, Vehicle


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['pk', 'registration', 'capacity',
                  'is_available', 'is_refrigerate']


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ['pk', 'origin', 'destination']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['pk', 'id_offer', 'route', 'need_refrigerate']
