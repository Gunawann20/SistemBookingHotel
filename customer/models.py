from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField 


class Customer(models.Model):
    GENDER = [
        ("MALE", "Male"),
        ("FEMALE", "Female")
    ]

    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    gender      = models.CharField(max_length=50, choices=GENDER)
    phone       = PhoneNumberField()
    address     = models.TextField()

    def __str__(self):
        return self.name
    


