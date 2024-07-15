from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer
from .serializers import CustomerCreateSerializer
from drf_yasg.utils import swagger_auto_schema


class CustomerViewSet(viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CustomerCreateSerializer)
    @action(detail=False, methods=['post'])
    def create_customer(self, request, *args, **kwargs):
        context = {
            'request': request
        }
        serializer = CustomerCreateSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "success create customer",
                "data": serializer.data
            }
            return Response(response, status=201)
        return Response(serializer.errors, status=400)

    
