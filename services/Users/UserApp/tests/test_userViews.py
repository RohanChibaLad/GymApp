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
        self.assertIn("message", body)

        me = self.client.get(self.user_url)
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json()["username"], "testuser")
        
    def test_missing_username(self):
        self.register_user()
        bad_payload = {
            "password": "ValidPass123*"
        }
        
        response = self.client.post(self.login_url, data=bad_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_USERNAME, response.json()["error"])
    
    def test_empty_username(self):
        self.register_user()
        bad_payload = {
            "username": " ",
            "password": "ValidPass123*"
        }
        
        response = self.client.post(self.login_url, data=bad_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_USERNAME, response.json()["error"])
    
    def test_invalid_username_type(self):
        self.register_user()
        bad_payload = {
            "username": 12345,
            "password": "ValidPass123*"
        }
        
        response = self.client.post(self.login_url, data=bad_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_USERNAME_TYPE, response.json()["error"]) 
    
    def test_missing_paswsword(self):
        self.register_user()
        bad_payload = {
            "username": "testuser"
        }
        
        response = self.client.post(self.login_url, data=bad_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.MISSING_PASSWORD, response.json()["error"])
    
    def test_empty_password(self):
        self.register_user()
        bad_payload = {
            "username": "testuser",
            "password": " "
        }
        
        response = self.client.post(self.login_url, data=bad_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.EMPTY_PASSWORD, response.json()["error"])
    
    def test_invalid_password_type(self):
        self.register_user()
        bad_payload = {
            "username": "testuser",
            "password": 123456
        }
        
        response = self.client.post(self.login_url, data=bad_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertIn(V.INVALID_PASSWORD_TYPE, response.json()["error"])       
        
    def test_wrong_username(self):
        self.register_user()
        wrong_payload = {
            "username": "wrongusername",
            "password": "ValidPass123*"
        }
        
        response = self.client.post(self.login_url, data=wrong_payload, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())
        self.assertIn("Invalid credentials", response.json()["error"])    

    def test_wrong_password(self):
        self.register_user()
        wrong_payload = {
            "username": "testuser",
            "password": "wrongpassword*"
        }
        
        response = self.client.post(self.login_url, data=wrong_payload, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())
        self.assertIn("Invalid credentials", response.json()["error"])  


class LogoutUserTests(TestCase):
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
    
    def login_user(self,payload=None):
        payload = payload or self.login_payload
        return self.post_json(self.login_url, payload)

    def test_url_exists(self):    
        response = self.client.get(self.logout_url)
        self.assertNotEqual(response.status_code, 404)

    def test_successful_logout(self):
        self.register_user()
        self.login_user()
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("User logged out successfully", response.json()["message"])  

    def test_unsuccessful_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 401)
        self.assertIn("User not logged in", response.json()["error"])  

    def test_double_logout(self):
        self.register_user()
        self.login_user()

        r1 = self.client.post(self.logout_url)
        self.assertEqual(r1.status_code, 200)

        r2 = self.client.post(self.logout_url)
        self.assertEqual(r2.status_code, 401)
        self.assertEqual(r2.json().get("error"), "User not logged in")
        me = self.client.get(self.user_url)
        self.assertEqual(me.status_code, 401)
        
class GetUserTests(TestCase):
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
    
    def get_json(self, url, data):
        return self.client.get(url, data=json.dumps(data), content_type="application/json")

    def register_user(self, payload=None):
        payload = payload or self.create_payload
        return self.post_json(self.user_url, payload)
    
    def login_user(self,payload=None):
        payload = payload or self.login_payload
        return self.post_json(self.login_url, payload)
    
    def test_url_exists(self):
        response = self.client.get(self.user_url)
        self.assertNotEqual(response.status_code, 404)
    
    def test_get_user_logged_in(self):
        self.register_user()
        self.login_user()
        response = self.client.get(self.user_url)
        body = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["username"], "testuser")
        self.assertEqual(body["email"], "testuser@email.com")
        self.assertEqual(body["phone_number"], "+447700900123")
        self.assertEqual(body["weight"], "70.50")
        self.assertEqual(body["height"], 180)
    
    def test_get_user_id_sucess(self):
        created = self.register_user().json()
        user_id = created["id"]
        response = self.client.get(self.user_url, {"id": user_id})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], user_id)
        
    def test_get_by_username_success(self):
        self.register_user()
        response = self.client.get(self.user_url, {"username": "testuser"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "testuser")
    
    def test_get_by_email_success_case_insensitive(self):
        self.register_user()
        response = self.client.get(self.user_url, {"email": "TestUser@Email.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "testuser@email.com")
    
    def test_get_by_id_invalid_type(self):
        self.register_user()
        response = self.client.get(self.user_url, {"id": "abc"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("User ID must be an integer.", response.json()["error"])

    def test_get_by_id_empty(self):
        self.register_user()
        response = self.client.get(self.user_url, {"id": ""})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(V.EMPTY_USER_ID, response.json()["error"])

    def test_get_by_id_not_found(self):
        self.register_user()
        response = self.client.get(self.user_url, {"id": 999999})
        
        self.assertEqual(response.status_code, 404)
        self.assertIn(V.ID_DOES_NOT_EXIST, response.json()["error"])        

    def test_get_by_username_empty(self):
        self.register_user()
        response = self.client.get(self.user_url, {"username": ""})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(V.EMPTY_USERNAME, response.json()["error"])

    def test_get_by_email_not_found(self):
        self.register_user()
        response = self.client.get(self.user_url, {"email": "missing@email.com"})
        
        self.assertEqual(response.status_code, 404)
        self.assertIn(V.EMAIL_DOES_NOT_EXIST, response.json()["error"])         
    
    def test_get_by_email_empty(self):
        self.register_user()
        response = self.client.get(self.user_url, {"email": ""})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(V.EMPTY_EMAIL, response.json()["error"])

    def test_get_by_invalid_email(self):
        self.register_user()
        response = self.client.get(self.user_url, {"email": "not-an-email"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(V.INVALID_EMAIL, response.json()["error"])       
    
    def test_get_by_id_gets_precedence(self):
        a = self.register_user().json()
        self.create_payload["username"] = "other"
        self.create_payload["email"] = "other@email.com"
        self.create_payload["phone_number"] = "+447700900124"
        b = self.register_user(self.create_payload).json()

        response = self.client.get(
            self.user_url,
            {"id": a["id"], "username": "other", "email": "other@email.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], a["id"])