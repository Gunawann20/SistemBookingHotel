from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Hotel(models.Model):
    name            = models.CharField(max_length=150)
    address         = models.TextField()
    phone           = PhoneNumberField()
    email           = models.EmailField(max_length=254, unique=True)
    description     = models.TextField()
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPE = {
        "STANDARD": "STANDARD",
        "SUPERIOR": "SUPERIOR",
        "DELUXE"  : "DELUXE"
    }

    STATUS = {
        "AVAILABLE": "AVAILABLE",
        "MAINTENANCE": "MAINTENANCE"
    }
    hotel           = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50)
    room_type       = models.CharField(max_length=50, choices=ROOM_TYPE)
    price           = models.IntegerField()
    availability    = models.CharField(max_length=50, choices= STATUS)
    description     = models.TextField()

    def __str__(self):
        return f"{self.hotel} - {self.name}"


class Media(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    media = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f"{self.hotel}"