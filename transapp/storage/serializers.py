from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Timespan, Warehouse, Action


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
        for action in obj.action_set.values():
            stats.append({'id_offer': action['id_offer'],
                         'action': action['action_type'], 'duration': action['duration']})
        return stats

    class Meta:
        model = get_user_model()
        fields = ['username', 'stats']


class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ['pk', 'name', 'action_available', 'openning_time', 'workers']


class WarehouseDetailSerializer(WarehouseSerializer):

    class Meta(WarehouseSerializer.Meta):
        fields = WarehouseSerializer.Meta.fields + ['description']


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ['pk', ]
