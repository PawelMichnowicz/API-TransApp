'''
Helper function used in storage app
'''
from rest_framework import serializers

def validate_action_window_date(serializer, warehouse):
    ''' validate if action window is located during opening time '''
    weekday_action = serializer.validated_data['monthday'].isoweekday()
    if (weekday_action not in [item['weekday'] for item in warehouse.openning_time.values()] or
        serializer.validated_data['from_hour'] < warehouse.openning_time.get(weekday=weekday_action).from_hour or
        serializer.validated_data['to_hour'] > warehouse.openning_time.get(weekday=weekday_action).to_hour):
        raise serializers.ValidationError('Action window is not consistent with openning time')