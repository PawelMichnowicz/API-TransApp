from rest_framework import serializers

from django.contrib.auth import get_user_model

from transport.serializers import TransportSerializer, OrderSerializer

from .models import OpenningTime, Timespan, Warehouse, Action


class TimespanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timespan
        fields = ['monthday', 'from_hour', 'to_hour', 'action_type']


class WarehouseWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'workplace']

    def validate(self, attrs):

        if not 'email' in attrs or not 'workplace' in attrs:
            raise serializers.ValidationError('You have to provide email and workplace')

        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email is already in use')

        return super().validate(attrs)


class WarehouserStatsSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField('calculate_stats')

    def calculate_stats(self, obj):
        stats = []
        for action in obj.action_set.values():
            stats.append({
                        'action': action['action_type'], 'status': action['status'], 'duration': action['duration']})
        return stats

    class Meta:
        model = get_user_model()
        fields = ['username', 'stats']


class OpenningTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenningTime
        fields = ['weekday', 'from_hour', 'to_hour']


class WarehouseSerializer(serializers.ModelSerializer):
    openning_time = OpenningTimeSerializer(many=True)
    timespan_available = TimespanSerializer(many=True, required=False)

    class Meta:
        model = Warehouse
        fields = ['pk', 'name', 'timespan_available', 'openning_time', 'workers']

    def validate(self, attrs):
        list_of_days = []
        if 'openning_time' in self.initial_data:
            openning_data = self.initial_data['openning_time']
            for openning_day in openning_data:
                openning_serializer = OpenningTimeSerializer(data=openning_day)
                openning_serializer.is_valid(raise_exception=True)
                list_of_days.append(openning_serializer.data['weekday'])
            if not (len(set(list_of_days)) == len(list_of_days)):
                raise serializers.ValidationError('You have to provided only one timespan per day')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        validated_data.pop('openning_time', None)
        validated_data.pop('timespan_available', None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data.pop('openning_time', None)
        validated_data.pop('timespan_available', None)
        return super().create(validated_data)


class ActionSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = Action
        fields = ['status', 'transport', 'action_type', 'workers', 'duration', 'warehouse']


class ActiopnOrderSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = ['pk', 'orders']

    def get_orders(self, obj):
        orders_queryset = obj.transport.orders
        serializer = OrderSerializer(orders_queryset, many=True)
        return serializer.data






