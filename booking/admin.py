from django.contrib import admin
from .models import Booking, Review

@admin.register(Booking)
class AdminBooking(admin.ModelAdmin):
    list_display = ['id', 'room', 'customer', 'check_in', 'check_out', 'status']

@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ['id', 'booking', 'review', 'rating']
