from rest_framework import serializers
from .models import Category, Hotel, Media, Room

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class HotelSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name') 
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'phone', 'email', 'description', 'category']

class MediaSerializer(serializers.HyperlinkedModelSerializer):
    hotel = serializers.SlugRelatedField(queryset=Hotel.objects.all(), slug_field='name')
    class Meta:
        model = Media
        fields = ['id', 'hotel', 'media']

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    hotel = serializers.SlugRelatedField(queryset=Hotel.objects.all(), slug_field='name')
    class Meta:
        model = Room
        fields = ['id', 'hotel', 'name', 'room_type', 'price', 'availability', 'description']
