from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserCreateSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    @swagger_auto_schema(request_body=UserCreateSerializer)
    @action(detail=False, methods=['post'])
    def create_user(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "success create user",
                "data": serializer.data
            }
            return Response(response, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=UserLoginSerializer)
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username= username, password= password)
            if user:
                login(request, user)
                response = {
                    'status': "success",
                    "message": "login successfuly",
                    "data": {
                        "username": user.username,
                        "email": user.email
                    }
                }
                return Response(response, status=200)
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        return Response(serializer.errors, status=400)
