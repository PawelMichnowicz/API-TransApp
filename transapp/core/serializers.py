'''
Serializers for the core API Views.
'''
from rest_framework import serializers

from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    ''' Serializer for the user object '''
    password2 = serializers.CharField(
        style={"input_type": 'password'}, write_only=True)
    password = serializers.CharField(
        style={"input_type": 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2']

    def validate(self, data):
        ''' Validate if passowrds are equal and if email is available'''
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Hasła nie są identyczne")
        if 'email' in data and get_user_model().objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email zajęty")
        if not 'email' in data :
            data['email'] = None
        return data

    def create(self, validated_data):
        ''' Create and return user with encrypted password '''
        user = get_user_model().objects.create_user(email=self.validated_data['email'],)
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


