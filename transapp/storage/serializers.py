from rest_framework import serializers
from .models import Warehouse, ReceiveAction, SendAction

class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ['pk', ]


class WarehouseDetailSerializer(WarehouseSerializer):

    class Meta(WarehouseSerializer.Meta):
        fields = WarehouseSerializer.Meta.fields + ['description']


class ReceiveActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiveAction
        fields = ['pk',]


class ReceiveActionDetailSerializer(ReceiveActionSerializer):

    class Meta(ReceiveActionSerializer.Meta):
        fields = ReceiveActionSerializer.Meta.fields + ['description']


class SendActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SendAction
        fields = ['pk',]


class SendActionDetailSerializer(SendActionSerializer):

    class Meta(SendActionSerializer.Meta):
        fields = SendActionSerializer.Meta.fields + ['description']