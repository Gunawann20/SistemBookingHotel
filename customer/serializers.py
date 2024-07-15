from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'gender', 'phone', 'address']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)