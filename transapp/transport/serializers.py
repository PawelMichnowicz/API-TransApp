from rest_framework import serializers
from .models import Route, AcceptedOffer, Offer, Vehicle


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['pk', 'registration', 'capacity', 'is_available', 'is_refrigerate']


class VehicleDetailSerializer(VehicleSerializer):

    class Meta(VehicleSerializer.Meta):
        fields = VehicleSerializer.Meta.fields + ['description']


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ['pk','origin', 'destination']


class RouteDetailSerializer(RouteSerializer):

    class Meta(RouteSerializer.Meta):
        fields = RouteSerializer.Meta.fields + ['description']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['pk','id_offer','route', 'need_refrigerate']


class OfferDetailSerializer(OfferSerializer):

    class Meta(OfferSerializer.Meta):
        fields = OfferSerializer.Meta.fields + ['description']


class AcceptedOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcceptedOffer
        fields = ['pk','id_offer', 'vehicle', 'route']

class AcceptedOfferDetailSerializer(AcceptedOfferSerializer):

    class Meta(AcceptedOfferSerializer.Meta):
        fields = AcceptedOfferSerializer.Meta.fields + ['description']