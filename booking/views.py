from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Booking, Review
from customer.models import Customer
from .serializers import BookingCreateSerializer, BookingUpdateSerializer, BookingListSerializer, ReviewSerializer
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'update']:
            return BookingUpdateSerializer
        elif self.action in ['list_booked_room']:
            return BookingListSerializer
        else:
            return BookingCreateSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'list_booked_room']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        check_in = serializer.validated_data.get('check_in', timezone.now())
        check_out = serializer.validated_data.get('check_out', timezone.now())

        if check_out <= check_in:
            return Response({"error": "Check-out date must be after check-in date."}, status=400)

        room = serializer.validated_data.get('room')

        is_booking = Booking.objects.filter(
            room=room,
            status__in=['PENDING', 'CONFIRMED', 'CHECKED_IN'],  
            check_out__gt=check_in,  
            check_in__lt=check_out   
        ).exists()

        if is_booking:
            response = {
                "status" : "Failed",
                "message": "Room is already booked during the requested dates."
            }
            return Response(response)

        customer = Customer.objects.get(user=request.user)

        if not customer:
            return Response({"error": "Your account is not yet registered as a customer"}, status=404)
        
        serializer.validated_data['customer'] = customer

        serializer.save()
        response = {
            "status"  : "Success",
            "message" : "Success booked room",
            "data"    : serializer.data
        }

        return Response(response, status=201)
    
    @action(detail=False, methods=['GET'])
    def list_booked_room(self, request, *args, **kwargs):
        booking_list = Booking.objects.filter(customer__user = request.user).select_related('room__hotel')
        serializer = self.get_serializer(booking_list, many=True)

        if booking_list.count() == 0:
            return Response({"error": "You don't have a booking history"}, status=404)

        response = {
            "status": "Success",
            "message": "Success get data",
            "data": serializer.data
        }

        return Response(response, status=200)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'get_average_rating']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        booking_id = request.data.get('booking')
        booking = Booking.objects.get(id=booking_id)
        if booking.customer.user != request.user:
            return Response({"error": "You are not allowed to review this booking"}, status=403)
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('room', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Room ID")
        ], responses={200: openapi.Response('Average rating', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'average_rating': openapi.Schema(type=openapi.TYPE_NUMBER)
            }
        ))}
    )
    @action(detail=False, methods=['GET'])
    def get_average_rating(self, request, *args, **kwargs):
        room_id = request.query_params.get('room')
        reviews = Review.objects.filter(booking__room_id=room_id)
        if reviews.count() == 0:
            return Response({"average_rating": 0}, status=200)
        total_rating = 0
        for review in reviews:
            total_rating += review.rating
        average_rating = total_rating / reviews.count()

        response = {
            "status"    : "Success",
            "message"   : "Success get average rating",
            "data"      : {
                "average_rating": round(average_rating, 1)
                }
        }
        return Response(response, status=200)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('room', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Room ID")
        ], responses={200: openapi.Response('Review list', openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'review': openapi.Schema(type=openapi.TYPE_STRING),
                    'rating': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
        ))}
    )
    @action(detail=False, methods=['GET'])
    def get_review_by_room(self, request, *args, **kwargs):
        room_id = request.query_params.get('room')
        reviews = Review.objects.filter(booking__room_id=room_id)
        print(reviews)
        serializer = self.get_serializer(reviews, many=True)

        if reviews.count() == 0:
            return Response({"error": "No review for this booking"}, status=404)

        response = {
            "status": "Success",
            "message": "Success get data",
            "data": serializer.data
        }

        return Response(response, status=200)



    


