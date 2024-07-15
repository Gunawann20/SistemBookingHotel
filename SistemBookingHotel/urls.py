from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from customer.views import CustomerViewSet
from hotel.views import CategoryViewSet, HotelViewSet, MediaViewSet, RoomViewSet
from booking.views import BookingViewSet, ReviewViewSet
from user.views import UserViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Sistem Booking Hotel API",
        default_version='v1',
        description="API documentation for Booking Hotels System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

router = routers.DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'user', UserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'hotel', HotelViewSet)
router.register(r'media', MediaViewSet)
router.register(r'room', RoomViewSet)
router.register(r'booking', BookingViewSet)
router.register(r'review', ReviewViewSet)

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
