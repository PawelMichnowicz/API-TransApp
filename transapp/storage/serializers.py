from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Timespan, Warehouse, Action


class TimespanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timespan
        fields = ['monthday', 'from_hour', 'to_hour', 'action']



class WarehouseWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'workplace']

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email is already in use')

        return super().validate(attrs)


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

    def validate(self, attrs):
        list_of_days = [item.weekday for item in attrs['openning_time']]
        if not (len(set(list_of_days)) == len(list_of_days)):
            raise serializers.ValidationError('You have to provided only one timespan per day')
        return super().validate(attrs)


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ['pk', ]
