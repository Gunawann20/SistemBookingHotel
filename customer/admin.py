from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'gender', 'phone', 'address']
