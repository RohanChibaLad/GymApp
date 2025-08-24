from decimal import Decimal
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from UserApp.viewHandling import viewHandlingValidators, viewHandlingConstants
import json
import BadRequest, ObjectDoesNotExist

USERNAME = "testuser"
EMAIL = "test@email.com"
PASSWORD = "TestPassword123*"
FIRST_NAME = "Test"
LAST_NAME = "User"
DATE_OF_BIRTH = date(2000, 1, 1)
PHONE_NUMBER = "+1234567890"
WEIGHT = Decimal("70.50")
HEIGHT = 180

USERNAME_2 = "testuser2"
EMAIL_2 = "test2@email.com"
PHONE_NUMBER_2 = "+1234567891"

class CreateUserCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user')  # Assuming 'user' is the name for userRegister view

    def test_create_user_success(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("User Created!", response.json())
        self.assertTrue(response.json()["User Created!"])
        self.assertIn("User ID", response.json())
        self.assertIn("Name", response.json())
        self.assertEqual(response.json()["Name"], FIRST_NAME)

    def test_create_user_missing_username(self):
        data = {
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_USERNAME, response.content.decode())

    def test_create_user_empty_username(self):
        data = {
            "username": "",
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_USERNAME, response.content.decode())
    
    def test_create_user_taken_username(self):
        get_user_model().objects.create_user(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            date_of_birth=DATE_OF_BIRTH,
            phone_number=PHONE_NUMBER,
            weight=WEIGHT,
            height=HEIGHT
        )

        data = {
            "username": USERNAME,
            "email": EMAIL_2,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.TAKEN_USERNAME, response.content.decode())  
        
    def test_create_user_invalid_username(self):
        data = {
            "username": "ab",  # Too short
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_USERNAME, response.content.decode())
    
    def test_create_user_invalid_username_type(self):
        data = {
            "username": 12345,  # Not a string
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_USERNAME_TYPE, response.content.decode())
    
    def test_create_user_missing_password(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_PASSWORD, response.content.decode())
    
    def test_create_user_empty_password(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": "",
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_PASSWORD, response.content.decode())
    
    def test_create_user_invalid_password(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": "short",  # Too short and simple
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_PASSWORD, response.content.decode())
        
    def test_create_user_uncomplex_password(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": "alllowercase",  # Lacks complexity
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.UNCOMPLEX_PASSWORD, response.content.decode())
    
    def test_create_user_password_contains_first_name(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": "TestPassword123*",  # Contains first name
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.FIRST_NAME_IN_PASSWORD, response.content.decode())
    
    def test_create_user_password_contains_last_name(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": "UserPassword123*",  # Contains last name
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.LAST_NAME_IN_PASSWORD, response.content.decode())
    
    def test_create_user_unaccepted_characters_in_password(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": "ValidPass123*<>",  # Contains unaccepted characters
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.UNACCEPTED_CHARACTERS_IN_PASSWORD, response.content.decode())
    
    def test_create_user_invalid_password_type(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": 12345678,  # Not a string
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_PASSWORD_TYPE, response.content.decode())
    
    def test_create_user_missing_first_name(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_FIRST_NAME, response.content.decode())
    
    def test_create_user_empty_first_name(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": "",
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_FIRST_NAME, response.content.decode())
    
    def test_create_user_invalid_first_name_type(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": 12345,  # Not a string
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_FIRST_NAME_TYPE, response.content.decode())
    
    def test_create_user_missing_last_name(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_LAST_NAME, response.content.decode())
    
    def test_create_user_empty_last_name(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": "",
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_LAST_NAME, response.content.decode())
    
    def test_create_user_invalid_last_name_type(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": 12345,  # Not a string
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_LAST_NAME_TYPE, response.content.decode())
    
    def test_create_user_missing_email(self):
        data = {
            "username": USERNAME,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_EMAIL, response.content.decode())
    
    def test_create_user_empty_email(self):
        data = {
            "username": USERNAME,
            "email": "",
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_EMAIL, response.content.decode())
    
    def test_create_user_invalid_email(self):
        data = {
            "username": USERNAME,
            "email": "not-an-email",  # Invalid email format
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_EMAIL, response.content.decode())
    
    def test_create_user_taken_email(self):
        get_user_model().objects.create_user(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            date_of_birth=DATE_OF_BIRTH,
            phone_number=PHONE_NUMBER,
            weight=WEIGHT,
            height=HEIGHT
        )

        data = {
            "username": USERNAME_2,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.TAKEN_EMAIL, response.content.decode())
    
    def test_create_user_invalid_email_type(self):
        data = {
            "username": USERNAME,
            "email": 12345,  # Not a string
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_EMAIL_TYPE, response.content.decode())
    
    def test_create_user_missing_date_of_birth(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_DATE_OF_BIRTH, response.content.decode())
    
    def test_create_user_empty_date_of_birth(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": "",
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_DATE_OF_BIRTH, response.content.decode())
    
    def test_create_user_invalid_date_of_birth(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": "invalid-date",  # Invalid date format
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_DATE_OF_BIRTH, response.content.decode())
    
    def test_create_user_future_date_of_birth(self):
        future_date = (date.today().replace(year=date.today().year + 1)).strftime("%Y-%m-%d")
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": future_date,  # Future date
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.FUTURE_DATE_OF_BIRTH, response.content.decode())
    
    def test_create_user_old_date_of_birth(self):
        old_date = (date.today().replace(year=date.today().year - 101)).strftime("%Y-%m-%d")
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": old_date,  # More than 100 years ago
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.OLD_DATE_OF_BIRTH, response.content.decode())
    
    def test_create_user_missing_phone_number(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_PHONE_NUMBER, response.content.decode())
    
    def test_create_user_empty_phone_number(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": "",
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_PHONE_NUMBER, response.content.decode())
    
    def test_create_user_invalid_phone_number(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": "invalid-phone",  # Invalid phone format
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_PHONE_NUMBER, response.content.decode())
    
    def test_create_user_taken_phone_number(self):
        get_user_model().objects.create_user(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            date_of_birth=DATE_OF_BIRTH,
            phone_number=PHONE_NUMBER,
            weight=WEIGHT,
            height=HEIGHT
        )

        data = {
            "username": USERNAME_2,
            "email": EMAIL_2,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.TAKEN_PHONE_NUMBER, response.content.decode())
    
    def test_create_user_invalid_phone_number_type(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": 1234567890,  # Not a string
            "weight": str(WEIGHT),
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_PHONE_NUMBER_TYPE, response.content.decode())
    
    def test_create_user_missing_weight(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_WEIGHT, response.content.decode())
    
    def test_create_user_empty_weight(self): 
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": "",
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_WEIGHT, response.content.decode())
    
    def test_create_user_invalid_weight(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": "invalid-weight",  # Not a decimal
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_WEIGHT, response.content.decode())
    
    def test_create_user_negative_weight(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": "-70.5",  # Negative weight
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.NEGATIVE_WEIGHT, response.content.decode())
    
    def test_create_user_large_weight_type(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(Decimal('1000.0')),  # Excessively large weight
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.LARGE_WEIGHT, response.content.decode())
    
    def test_create_user_invalid_weight_type(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": ["70.5"],  # Not a string or number
            "height": HEIGHT
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_WEIGHT_TYPE, response.content.decode())
    
    def test_create_user_missing_height(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT)
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.MISSING_HEIGHT, response.content.decode())
    
    def test_create_user_empty_height(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": ""
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.EMPTY_HEIGHT, response.content.decode())
    
    def test_create_user_invalid_height(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": "invalid-height"  # Not an integer
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_HEIGHT, response.content.decode())
    
    def test_create_user_negative_height(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": -180  # Negative height
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.NEGATIVE_HEIGHT, response.content.decode())
    
    def test_create_user_large_height(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": 300  # Excessively large height
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.LARGE_HEIGHT, response.content.decode())
    
    def test_create_user_invalid_height_type(self):
        data = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "first_name": FIRST_NAME,
            "last_name": LAST_NAME,
            "date_of_birth": DATE_OF_BIRTH.strftime("%Y-%m-%d"),
            "phone_number": PHONE_NUMBER,
            "weight": str(WEIGHT),
            "height": 180.5  # Not an integer
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(viewHandlingConstants.INVALID_HEIGHT_TYPE, response.content.decode())