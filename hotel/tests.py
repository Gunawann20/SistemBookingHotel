from django.test import TestCase
from .models import Hotel

class HotelTestCase(TestCase):
    def setUp(self):
        Hotel.objects.create(name="Hotel 1", address="Address 1", phone_number="1234567890", email="")

    def test_list_hotel(self):
        hotels = Hotel.objects.all()
        self.assertEqual(hotels.count(), 1)
