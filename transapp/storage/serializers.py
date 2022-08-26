"""
Serializers for storage APIs
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from transport.models import Order
from transport.serializers import OrderSerializer, TransportSerializer

from .models import Action, ActionWindow, OpenningTime, Warehouse


class ActionWindowSerializer(serializers.ModelSerializer):
    ''' Serializer for action window views '''
    class Meta:
        model = ActionWindow
        fields = ['monthday', 'from_hour',
                  'to_hour', 'action_type', 'warehouse']


class WorkerStatsSerializer(serializers.ModelSerializer):
    ''' Serializer for worker stats view '''
    stats = serializers.SerializerMethodField('include_stats')

    class Meta:
        model = get_user_model()
        fields = ['email', 'stats']

    def include_stats(self, obj):
        ''' Add warehouser stats into field '''
        stats = []
        for action in obj.action_set.values():
            stats.append({
                'action': action['action_type'], 'status': action['status'], 'duration': action['duration']})
        return stats


class OpenningTimeSerializer(serializers.ModelSerializer):
    ''' Serializer for openning time views '''
    class Meta:
        model = OpenningTime
        fields = ['weekday', 'from_hour', 'to_hour', 'warehouse']
        extra_kwargs = {"warehouse": {"required": False, "allow_null": True}}


class WarehouseSerializer(serializers.ModelSerializer):
    ''' Serializer for warehouse views '''
    openning_time = OpenningTimeSerializer(many=True)

    class Meta:
        model = Warehouse
        fields = ['pk', 'name', 'openning_time', 'workers']

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
    ''' Serializer for Actions '''
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = Action
        fields = ['pk', 'status', 'transport', 'action_type',
                  'workers', 'duration', 'warehouse']


class ActionOrderSerializer(serializers.ModelSerializer):
    ''' Serializer for detail about order in action '''
    orders = serializers.SerializerMethodField('get_orders')

    class Meta:
        model = Action
        fields = ['pk', 'orders']

    def get_orders(self, obj):
        ''' add infomation about orderd into field '''
        orders_queryset = obj.transport.orders
        serializer = OrderSerializer(orders_queryset, many=True)
        return serializer.data


class BrokenOrdersSerializer(serializers.ModelSerializer):
    ''' Helper serializer to create nested serializerr '''
    class Meta:
        model = Order
        fields = ['order_id']


class ActionAcceptSerializer(serializers.ModelSerializer):
    ''' Serializer for accept action view '''
    broken_orders = BrokenOrdersSerializer(many=True, required=False)

    class Meta:
        model = Action
        fields = ['broken_orders', 'duration', 'workers']

