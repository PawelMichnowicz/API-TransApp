from rest_framework import serializers

from django.contrib.auth import get_user_model

from transport.serializers import TransportSerializer, OrderSerializer

from storage.constants import StatusChoice

from .models import OpenningTime, ActionWindow, Warehouse, Action

import datetime


class ActionWindowSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionWindow
        fields = ['monthday', 'from_hour',
                  'to_hour', 'action_type', 'warehouse']


class ActionWindowCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionWindow
        fields = ['monthday', 'from_hour', 'to_hour', 'action_type']


class WarehouseWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'workplace']

    def validate(self, attrs):

        if not 'email' in attrs or not 'workplace' in attrs:
            raise serializers.ValidationError(
                'You have to provide email and workplace')

        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email is already in use')

        return super().validate(attrs)


# class WarehouseStatsSerializer(serializers.ModelSerializer):
#     stats = serializers.SerializerMethodField('calculate_stats')

#     class Meta:
#         model = Warehouse
#         fields = ['name',  'stats']

#     def calculate_stats(self, obj):
#         stats = {'num_of_deliver': 0, 'broken_deliver': 0}
#         sum_duration = datetime.timedelta(0)
#         for action in obj.actions.values():
#             stats['num_of_deliver'] += 1
#             if action["status"] == StatusChoice.DELIVERED_BROKEN:
#                 stats['broken_deliver'] += 1
#             sum_duration += action['duration']
#         try:
#             stats['average_duration'] = str(
#                 sum_duration / stats['num_of_deliver'])
#         except ZeroDivisionError:
#             stats['average_duration'] = None
#         return stats


class WorkerStatsSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField('calculate_stats')

    class Meta:
        model = get_user_model()
        fields = ['username', 'stats']

    def calculate_stats(self, obj):
        stats = []
        for action in obj.action_set.values():
            stats.append({
                'action': action['action_type'], 'status': action['status'], 'duration': action['duration']})
        return stats


class OpenningTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenningTime
        fields = ['weekday', 'from_hour', 'to_hour', 'warehouse']
        extra_kwargs = {"warehouse": {"required": False, "allow_null": True}}


class WarehouseSerializer(serializers.ModelSerializer):
    openning_time = OpenningTimeSerializer(many=True)
    action_window = ActionWindowCreateSerializer(many=True, required=False)

    class Meta:
        model = Warehouse
        fields = ['pk', 'name', 'action_window',
                  'openning_time', 'workers']

    def validate(self, attrs):
        ''' Validate if valid oppening time provided '''
        list_of_days = []
        if 'openning_time' in self.initial_data:
            openning_data = self.initial_data['openning_time']
            for openning_day in openning_data:
                openning_serializer = OpenningTimeSerializer(data=openning_day)
                openning_serializer.is_valid(raise_exception=True)
                list_of_days.append(openning_serializer.data['weekday'])
            if not (len(set(list_of_days)) == len(list_of_days)):
                raise serializers.ValidationError(
                    'You have to provided only one action window per day')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        ''' Drop openning time and action window from validated data to handle nested serializer '''
        validated_data.pop('openning_time', None)
        validated_data.pop('action_window', None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        ''' Drop openning time from validated data to handle nested serializer and check if action window isn't in request data'''
        validated_data.pop('openning_time', None)
        if 'action_window' in validated_data:
            raise serializers.ValidationError('You cannot include action window during create process')
        return super().create(validated_data)


class ActionSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = Action
        fields = ['pk', 'status', 'transport', 'action_type',
                  'workers', 'duration', 'warehouse']


class ActionOrderSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = ['pk', 'orders']

    def get_orders(self, obj):
        orders_queryset = obj.transport.orders
        serializer = OrderSerializer(orders_queryset, many=True)
        return serializer.data
