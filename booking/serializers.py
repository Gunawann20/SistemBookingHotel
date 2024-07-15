from rest_framework import serializers
from .models import Booking, Room, Review

class BookingCreateSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.filter(availability=Room.STATUS["AVAILABLE"]))
    class Meta:
        model = Booking
        fields = ['id','room', 'check_in', 'check_out']

class BookingUpdateSerializer(serializers.HyperlinkedModelSerializer):
    room  = serializers.CharField(source='room.name', read_only=True)
    customer = serializers.CharField(source='customer.name', read_only=True)
    class Meta:
        model = Booking
        fields = ['id','room', 'customer', 'check_in', 'check_out', 'status']

class BookingListSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField(source='room.hotel.name', read_only=True)
    room  = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id','hotel', 'room','check_in', 'check_out', 'status']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'review', 'rating']
