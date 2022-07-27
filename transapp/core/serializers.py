from rest_framework import serializers
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": 'password'}, write_only=True)
    password = serializers.CharField(
        style={"input_type": 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Hasła nie są identyczne")
        if get_user_model().objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email zajęty")
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(email=self.validated_data['email'],
                    username=self.validated_data['username'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
