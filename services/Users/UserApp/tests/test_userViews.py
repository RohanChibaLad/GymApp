from datetime import datetime
import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from UserApp.viewHandling import viewHandlingConstants as C

User = get_user_model()

class CreateUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('user')  # URL for user registration
        
    def payload(self, **overrides):
        data = {
            "username": "testuser",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@gmail.com@",
            "date_of_birth": date(2000, 1, 1),
            "phone_number": "+1234567890",
            "weight": Decimal("70.5"),
            "height": 180
        }
        
        data.update(overrides)
        return data
    
    def post(self, **overrides):
        return self.client.post(
            self.url,
            data=json.dumps(self.payload(**overrides)),
            content_type='application/json'
        )