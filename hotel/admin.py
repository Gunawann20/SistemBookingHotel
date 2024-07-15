from django.contrib import admin
from .models import Category, Hotel, Room, Media

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Hotel)
class AdminHotel(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone', 'email', 'description', 'category']

@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ['id', 'hotel', 'name', 'room_type', 'price', 'availability', 'description']

@admin.register(Media)
class AdminMedia(admin.ModelAdmin):
    list_display = ['id', 'hotel', 'media']