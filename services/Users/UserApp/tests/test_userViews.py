# UserApp/tests/test_views_create_user.py
from decimal import Decimal
from datetime import date, timedelta
import json

from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model

# If you assert on specific error texts, import your constants:
from UserApp.viewHandling import viewHandlingConstants as V

User = get_user_model()


class CreateUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.url = reverse("user")     
        except NoReverseMatch:
            self.url = "/user/"            

        self.payload = {
            "username": "testuser",
            "password": "ValidPass123*",
            "first_name": "Test",
            "last_name": "User",
            "email": "TestUser@Email.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "+447700900123",
            "weight": 70.5,
            "height": 180
        }

    def post_json(self, data):
        return self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
    
    def test_url_exists(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 404)
    
    def test_invalid_json(self):
        response = self.client.post(
            self.url,
            data="Not a JSON",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
    
    def test_create_user_success(self):
        response = self.post_json(self.payload)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn("ok", response_data)
        self.assertTrue(response_data["ok"])
        self.assertIn("id", response_data)
        self.assertIn("name", response_data)
        self.assertEqual(response_data["name"], "Test")

        user = User.objects.get(id=response_data["id"])
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("ValidPass123*"))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertEqual(user.date_of_birth, date(2000, 1, 1))
        self.assertEqual(user.phone_number, "+447700900123")
        self.assertEqual(user.weight, 70.5)
        self.assertEqual(user.height, 180)
        
    def test_create_user_trims_fields(self):
        payload = self.payload.copy()
        payload["username"] = " testuser "
        payload["first_name"] = "  Test  "
        payload["last_name"] = "  User  "
        payload["email"] = "    TestUser@email.com   "
        payload["phone_number"] = "   +447700900123   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 201)
        
        user = User.objects.get(id=response.json()["id"])
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertEqual(user.phone_number, "+447700900123")   
    
    def test_missing_username(self):
        payload = self.payload.copy()
        del payload["username"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_USERNAME, response.json()["error"])
    
    def test_empty_username(self):
        payload = self.payload.copy()
        payload["username"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_USERNAME, response.json()["error"])
    
    def test_invalid_username_type(self):
        payload = self.payload.copy()
        payload["username"] = 12345
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_USERNAME_TYPE, response.json()["error"])    
    
    def test_taken_username(self):
        payload = self.payload.copy()
        payload["email"] = "testuser2@email.com"
        payload["phone_number"] = "+447700900124"
        self.post_json(payload)  # Create first user
        
        response = self.post_json(payload)  # Try to create second user with same username
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.TAKEN_USERNAME, response.json()["error"])   
    
    def test_missing_password(self):
        payload = self.payload.copy()
        del payload["password"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_PASSWORD, response.json()["error"])
    
    def test_empty_password(self):
        payload = self.payload.copy()
        payload["password"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_PASSWORD, response.json()["error"])
    
    def test_invalid_password_type(self):
        payload = self.payload.copy()
        payload["password"] = 12345678
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_PASSWORD_TYPE, response.json()["error"])
    
    def test_password_too_short(self):
        payload = self.payload.copy()
        payload["password"] = "Short1*"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_PASSWORD, response.json()["error"])
    
    def test_password_too_simple(self):
        payload = self.payload.copy()
        payload["password"] = "alllowercase"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.UNCOMPLEX_PASSWORD, response.json()["error"])
    
    def test_password_contains_first_name(self):
        payload = self.payload.copy()
        payload["password"] = "Test123*"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.FIRST_NAME_IN_PASSWORD, response.json()["error"])
    
    def test_password_contains_last_name(self):
        payload = self.payload.copy()
        payload["password"] = "User123*"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.LAST_NAME_IN_PASSWORD, response.json()["error"])
    
    def test_password_unaccepted_characters(self):
        payload = self.payload.copy()
        payload["password"] = "Valid Pass123*"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.UNACCEPTED_CHARACTERS_IN_PASSWORD, response.json()["error"])
    
    def test_missing_first_name(self):
        payload = self.payload.copy()
        del payload["first_name"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_FIRST_NAME, response.json()["error"])
    
    def test_empty_first_name(self):
        payload = self.payload.copy()
        payload["first_name"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_FIRST_NAME, response.json()["error"])
    
    def test_invalid_first_name_type(self):
        payload = self.payload.copy()
        payload["first_name"] = 12345
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_FIRST_NAME_TYPE, response.json()["error"])
    
    def test_missing_last_name(self):
        payload = self.payload.copy()
        del payload["last_name"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_LAST_NAME, response.json()["error"])
    
    def test_empty_last_name(self):
        payload = self.payload.copy()
        payload["last_name"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_LAST_NAME, response.json()["error"])
    
    def test_invalid_last_name_type(self):
        payload = self.payload.copy()
        payload["last_name"] = 12345
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_LAST_NAME_TYPE, response.json()["error"])
    
    def test_missing_email(self):
        payload = self.payload.copy()
        del payload["email"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_EMAIL, response.json()["error"])
    
    def test_empty_email(self):
        payload = self.payload.copy()
        payload["email"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_EMAIL, response.json()["error"])
    
    def test_invalid_email_type(self):
        payload = self.payload.copy()
        payload["email"] = 12345
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_EMAIL_TYPE, response.json()["error"])
    
    def test_invalid_email_format(self):
        payload = self.payload.copy()
        payload["email"] = "not-an-email"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_EMAIL, response.json()["error"])
    
    def test_taken_email(self):
        first = self.payload.copy()
        first["username"] = "user_a"
        first["email"] = "dup@email.com"
        first["phone_number"] = "+447700900124"
        self.post_json(first)

        second = self.payload.copy()
        second["username"] = "user_b"              
        second["email"] = "dup@email.com"          
        second["phone_number"] = "+447700900125"  
        resp = self.post_json(second)

        self.assertEqual(resp.status_code, 400)
        self.assertIn(V.TAKEN_EMAIL, resp.json()["error"])
    
    def test_missing_date_of_birth(self):
        payload = self.payload.copy()
        del payload["date_of_birth"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_DATE_OF_BIRTH, response.json()["error"])
    
    def test_empty_date_of_birth(self):
        payload = self.payload.copy()
        payload["date_of_birth"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_DATE_OF_BIRTH, response.json()["error"])
    
    def test_invalid_date_of_birth_type(self):
        payload = self.payload.copy()
        payload["date_of_birth"] = 12345
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_DATE_OF_BIRTH, response.json()["error"])
    
    def test_invalid_date_of_birth_format(self):
        payload = self.payload.copy()
        payload["date_of_birth"] = "01-01-2000"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_DATE_OF_BIRTH, response.json()["error"])
    
    def test_future_date_of_birth(self):
        payload = self.payload.copy()
        future_date = (date.today() + timedelta(days=1)).isoformat()
        payload["date_of_birth"] = future_date
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.FUTURE_DATE_OF_BIRTH, response.json()["error"])
    
    def test_too_old_date_of_birth(self):
        payload = self.payload.copy()
        old_date = (date.today() - timedelta(days=36525 + 1)).isoformat()
        payload["date_of_birth"] = old_date
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.OLD_DATE_OF_BIRTH, response.json()["error"])
    
    def test_missing_phone_number(self):
        payload = self.payload.copy()
        del payload["phone_number"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_PHONE_NUMBER, response.json()["error"])
    
    def test_empty_phone_number(self):
        payload = self.payload.copy()
        payload["phone_number"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_PHONE_NUMBER, response.json()["error"])
    
    def test_invalid_phone_number_type(self):
        payload = self.payload.copy()
        payload["phone_number"] = 12345
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_PHONE_NUMBER_TYPE, response.json()["error"])
    
    def test_invalid_phone_number_format(self):
        payload = self.payload.copy()
        payload["phone_number"] = "not-a-phone-number"
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_PHONE_NUMBER, response.json()["error"])
    
    def test_taken_phone_number(self):
        first = self.payload.copy()
        first["username"] = "user_c"
        first["email"] = "unique1@email.com"
        first["phone_number"] = "+447700900126"
        self.post_json(first)

        second = self.payload.copy()
        second["username"] = "user_d"                  
        second["email"] = "unique2@email.com"           
        second["phone_number"] = "+447700900126"       
        resp = self.post_json(second)

        self.assertEqual(resp.status_code, 400)
        self.assertIn(V.TAKEN_PHONE_NUMBER, resp.json()["error"])

    
    def test_missing_weight(self):
        payload = self.payload.copy()
        del payload["weight"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_WEIGHT, response.json()["error"])   
    
    def test_empty_weight(self):    
        payload = self.payload.copy()
        payload["weight"] = "   "
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_WEIGHT, response.json()["error"]) 
    
    def test_invalid_weight_type(self):
        payload = self.payload.copy()
        payload["weight"] = ["70.5"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_WEIGHT_TYPE, response.json()["error"])
    
    def test_negative_weight(self):
        payload = self.payload.copy()
        payload["weight"] = -1
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.SMALL_WEIGHT, response.json()["error"])
    
    def test_too_large_weight(self):
        payload = self.payload.copy()
        payload["weight"] = 501
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.LARGE_WEIGHT, response.json()["error"])
    
    def test_missing_height(self):
        payload = self.payload.copy()
        del payload["height"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_HEIGHT, response.json()["error"])
    
    def test_empty_height(self):    
        payload = self.payload.copy()
        payload["height"] = ""
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_HEIGHT, response.json()["error"])
    
    def test_invalid_height_type(self):
        payload = self.payload.copy()
        payload["height"] = ["180"]
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_HEIGHT_TYPE, response.json()["error"])
    
    def test_too_small_height(self):
        payload = self.payload.copy()
        payload["height"] = 39
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.SMALL_HEIGHT, response.json()["error"])
    
    def test_too_large_height(self):
        payload = self.payload.copy()
        payload["height"] = 301
        
        response = self.post_json(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.LARGE_HEIGHT, response.json()["error"])
    
    
class LoginUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user_url = reverse("user")
        except NoReverseMatch:
            self.user_url = "/user/"
        try:
            self.login_url = reverse("login")
        except NoReverseMatch:
            self.login_url = "/login/"
        try:
            self.logout_url = reverse("logout")
        except NoReverseMatch:
            self.logout_url = "/logout/"

        self.create_payload = {
            "username": "testuser",
            "password": "ValidPass123*",
            "first_name": "Test",
            "last_name": "User",
            "email": "TestUser@Email.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "+447700900123",
            "weight": 70.5,
            "height": 180,
        }
        self.login_payload = {
            "username": "testuser",
            "password": "ValidPass123*",
        }

    def post_json(self, url, data):
        return self.client.post(url, data=json.dumps(data), content_type="application/json")

    def register_user(self, payload=None):
        payload = payload or self.create_payload
        return self.post_json(self.user_url, payload)

    def test_url_exists(self):    
        response = self.client.get(self.login_url)
        self.assertNotEqual(response.status_code, 404)
    
    def test_invalid_json(self):
        response = self.client.post(self.login_url, data="not json", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
    
    def test_successful_login(self):
        self.register_user()
        response = self.client.post(self.login_url, data=self.login_payload, content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["username"], "testuser")
        self.asssertIn("message", body)