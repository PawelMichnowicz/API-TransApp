import json

from rest_framework import serializers
from rest_framework.utils import model_meta

from django.contrib.auth import get_user_model

from .models import OpenningTime, Timespan, Warehouse, Action


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


class OpenningTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenningTime
        fields = ['weekday', 'from_hour', 'to_hour']

class WarehouseSerializer(serializers.ModelSerializer):
    openning_time = OpenningTimeSerializer(many=True, read_only=True)

    class Meta:
        model = Warehouse
        fields = ['pk', 'name', 'action_available', 'openning_time', 'workers']

    def validate(self, attrs):

        list_of_days = []
        if 'openning_time' in self.initial_data:
            openning_data = self.initial_data['openning_time']
            attrs['openning_time'] = []
            for openning_day in openning_data:
                openning_serializer = OpenningTimeSerializer(data=openning_day)
                if not openning_serializer.is_valid():
                    raise serializers.ValidationError(openning_serializer.errors)
                attrs['openning_time'].append(openning_serializer.data)

                list_of_days.append(openning_serializer.data['weekday'])
            if not (len(set(list_of_days)) == len(list_of_days)):
                raise serializers.ValidationError('You have to provided only one timespan per day')

        return super().validate(attrs)


    def update(self, instance, validated_data, **args):
        # sprobuje perform update  
        openning_time = validated_data['openning_time']
        instance.openning_time.clear()
        for openning_day in openning_time:
            day_obj = OpenningTime.objects.filter(
                weekday=openning_day['weekday'],
                from_hour=openning_day['from_hour'],
                to_hour=openning_day['to_hour'],
                ).first()
            if not day_obj:
                serializer = OpenningTimeSerializer(data=openning_day)
                serializer.is_valid(raise_exception=True)
                day_obj = serializer.save()
            instance.openning_time.add(day_obj)
        instance.save()

        return instance

class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ['pk', ]
