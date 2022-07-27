from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Timespan, Warehouse, ReceiveAction, SendAction

ACTIONS = ['send', 'receive']


class TimespanSerializer(serializers.ModelSerializer):

    action = serializers.CharField(required=False)

    class Meta:
        model = Timespan
        fields = ['monthday', 'from_hour', 'to_hour', 'action']

    def save(self, **kwargs):
        return super().save(**kwargs)


class WarehouseWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'workplace']


class WarehouserStatsSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField('calculate_stats')

    def calculate_stats(self, obj):
        {
            "president": {
                "name": "Zaphod Beeblebrox",
                "species": "Betelgeusian"
            }
        }
        stats = []
        for send_action in obj.sendaction_set.all():
            stats.append({'id_offer': send_action.id_offer,
                         'action': 'send', 'duration': send_action.duration})
        for receive_action in obj.receiveaction_set.all():
            stats.append({'id_offer': receive_action.id_offer,
                         'action': 'receive', 'duration': receive_action.duration})
        return stats

    class Meta:
        model = get_user_model()
        fields = ['username', 'stats']


class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ['pk', 'name', 'receive_available',
                  'send_available', 'openning_time', 'workers']


class WarehouseDetailSerializer(WarehouseSerializer):

    class Meta(WarehouseSerializer.Meta):
        fields = WarehouseSerializer.Meta.fields + ['description']


class ReceiveActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiveAction
        fields = ['pk', ]


class ReceiveActionDetailSerializer(ReceiveActionSerializer):

    class Meta(ReceiveActionSerializer.Meta):
        fields = ReceiveActionSerializer.Meta.fields + ['description']


class SendActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SendAction
        fields = ['pk', ]


class SendActionDetailSerializer(SendActionSerializer):

    class Meta(SendActionSerializer.Meta):
        fields = SendActionSerializer.Meta.fields + ['description']
