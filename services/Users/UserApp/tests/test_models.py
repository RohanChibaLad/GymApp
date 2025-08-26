from decimal import Decimal
from datetime import date
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()


class UserModelBasicsTests(TestCase):
    def test_create_user_and_str(self):
        u = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="TestPassword123*",
            first_name="Test",
            last_name="User",
            date_of_birth=date(2000, 1, 1),
            phone_number="+1234567890",
            weight=Decimal("70.50"),
            height=180,
        )
        self.assertTrue(u.check_password("TestPassword123*"))  # password hashed
        self.assertEqual(str(u), "testuser")
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_staff)
        self.assertFalse(u.is_superuser)

    def test_create_superuser_flags(self):
        su = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="Pass123*",
        )
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)


class UserUniquenessTests(TransactionTestCase):
    reset_sequences = True  # use DB transactions for IntegrityError

    def test_unique_email(self):
        User.objects.create_user(username="user1", email="test@example.com", password="x")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="user2", email="test@example.com", password="x")

    def test_unique_username(self):
        User.objects.create_user(username="user1", email="test1@example.com", password="x")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="user1", email="test2@example.com", password="x")

    def test_unique_phone_number(self):
        User.objects.create_user(username="user1", email="test@example.com", phone_number="+1234567890", password="x")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="user2", email="test2@example.com", phone_number="+1234567890", password="x")
    
class UserFieldValidationTests(TestCase):
    def test_email_format_invalid_on_full_clean(self):
        u = User(username="bademail", email="not-an-email")
        u.set_password("x")
        with self.assertRaises(ValidationError):
            u.full_clean()  # EmailField validator runs here

    def test_phone_number_regex(self):
        ok = User(username="p1", email="p1@example.com", phone_number="+447700900123")
        ok.set_password("x")
        ok.full_clean()  # no raise

        bad = User(username="p2", email="p2@example.com", phone_number="invalidphone")
        bad.set_password("x")
        with self.assertRaises(ValidationError):
            bad.full_clean()

        # blank/None allowed by your model
        none_ok = User(username="p3", email="p3@example.com", phone_number=None)
        none_ok.set_password("x")
        none_ok.full_clean()

        blank_ok = User(username="p4", email="p4@example.com", phone_number="")
        blank_ok.set_password("x")
        blank_ok.full_clean()

    def test_weight_min_and_decimal_places(self):
        u = User(username="w1", email="w1@example.com", weight=Decimal("-0.01"))
        u.set_password("x")
        with self.assertRaises(ValidationError):
            u.full_clean()

        u.weight = Decimal("72.345")  # too many decimal places for decimal_places=2
        with self.assertRaises(ValidationError):
            u.full_clean()

        # ok values
        u.username, u.email = "w_ok", "w_ok@example.com"
        u.weight = Decimal("72.40")
        u.full_clean()

    def test_height_bounds_on_full_clean(self):
        u = User(username="h1", email="h1@example.com", height=39)
        u.set_password("x")
        with self.assertRaises(ValidationError):
            u.full_clean()

        u.height = 301
        with self.assertRaises(ValidationError):
            u.full_clean()

        # boundary values ok
        u.username, u.email, u.height = "h_ok_40", "h_ok_40@example.com", 40
        u.full_clean()
        u.username, u.email, u.height = "h_ok_300", "h_ok_300@example.com", 300
        u.full_clean()


class UserMetaTests(TestCase):
    def test_ordering_by_username(self):
        User.objects.create_user(username="zeta",  email="z@e.com", password="x")
        User.objects.create_user(username="alpha", email="a@a.com", password="x")
        User.objects.create_user(username="mike",  email="m@m.com", password="x")
        usernames = [u.username for u in User.objects.all()]
        self.assertEqual(usernames, ["alpha", "mike", "zeta"])
