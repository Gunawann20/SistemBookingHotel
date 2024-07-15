from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from hotel.models import Room
from customer.models import Customer

class Booking(models.Model):
    STATUS = BOOKING_STATUS = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CHECKED_IN", "Checked In"),
        ("CHECKED_OUT", "Checked Out"),
        ("CANCELLED", "Cancelled")
    ]

    room            = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in        = models.DateTimeField()
    check_out       = models.DateTimeField()
    status          = models.CharField(max_length=50, choices=BOOKING_STATUS, default="PENDING")

    def __str__(self):
        return f"{self.room} - {self.customer} - {self.status}"

class Review(models.Model):
    booking     = models.ForeignKey(Booking, on_delete=models.CASCADE) 
    review      = models.TextField()
    rating      = models.IntegerField()

    def __str__(self):
        return f"{self.booking}"
