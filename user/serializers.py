from rest_framework import serializers
from django.contrib.auth.models import User

class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username    = validated_data['username'],
            email       = validated_data['email'],
            password    = validated_data['password']
        )

        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)