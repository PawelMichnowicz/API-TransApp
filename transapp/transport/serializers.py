from rest_framework import serializers
from .models import Route, AcceptedOffer, Offer, Vehicle


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['pk', 'registration', 'capacity', 'is_available', 'is_refrigerate']



class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ['pk','origin', 'destination']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['pk','id_offer','route', 'need_refrigerate']


class AcceptedOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcceptedOffer
        fields = ['pk','id_offer', 'vehicle', 'route']