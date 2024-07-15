from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import CategorySerializer, HotelSerializer, MediaSerializer, RoomSerializer
from .models import Category, Hotel, Media, Room
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        else: 
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class HotelViewSet(viewsets.ModelViewSet):
    queryset            = Hotel.objects.all()
    serializer_class    = HotelSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class MediaViewSet(viewsets.ModelViewSet):
    queryset            = Media.objects.all()
    serializer_class    = MediaSerializer
    parser_classes      = [MultiPartParser, FormParser]
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @extend_schema(
        request=MediaSerializer,
        responses={201: MediaSerializer},
        description="Endpoint to upload media files."
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class RoomViewSet(viewsets.ModelViewSet):
    queryset            = Room.objects.all()
    serializer_class    = RoomSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_room_available']:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('check_in', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Check-in datetime in format 'YYYY-MM-DDTHH:mm:ss'"),
            openapi.Parameter('check_out', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Check-out datetime in format 'YYYY-MM-DDTHH:mm:ss'")
        ],
        responses={200: RoomSerializer(many=True)}
    )
    @action(detail=False, methods=['GET'])
    def get_room_available(self, request, *args, **kwargs):
        check_in = request.query_params.get('check_in', timezone.now())
        check_out = request.query_params.get('check_out', timezone.now() + timedelta(days=1))

        if check_out <= check_in:
            return Response({"error": "Check-out date must be after check-in date."}, status=400)

        rooms = Room.objects.filter(
            availability=Room.STATUS["AVAILABLE"]
        ).exclude(
            Q(booking__check_in__lt=check_out, booking__check_out__gt=check_in) |
            Q(booking__check_in__gte=check_in, booking__check_in__lt=check_out) |
            Q(booking__check_out__gt=check_in, booking__check_out__lte=check_out) |
            Q(booking__check_in=check_in) |
            Q(booking__check_out=check_out)
        )

        serializer = self.get_serializer(rooms, many=True)

        if rooms.count() == 0:
            return Response({"error": "No room available for the selected date."}, status=400)

        response = {
            "status": "Success",
            "message": "Success get data",
            "data": serializer.data
        }

        return Response(response, status=200)