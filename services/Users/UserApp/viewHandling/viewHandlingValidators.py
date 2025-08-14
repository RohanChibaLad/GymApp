from UserApp.models import User  # Importing the custom User model 
from django.core.exceptions import ValidationError, BadRequest
from django.core.validators import validate_email, RegexValidator

from UserApp.viewHandling import viewHandlingConstants as validators  # Importing validation messages
import datetime


def validateUsername(data):
    """
    Validates the username field in the provided data.
    """
    username = data.get("username")
    
    if username is None:
        raise BadRequest(validators.MISSING_USERNAME)
    
    if not username.strip():
        raise BadRequest(validators.EMPTY_USERNAME)
    
    if User.objects.filter(username=username).exists():
        raise BadRequest(validators.TAKEN_USERNAME)
    
    if len(username) < 3 or len(username) > 150:
        raise BadRequest(validators.INVALID_USERNAME)


def validatePassword(data):
    """
    Validates the password field in the provided data.
    """
    password = data.get("password")
    
    if password is None:
        raise BadRequest(validators.MISSING_PASSWORD)
    
    if not password.strip():
        raise BadRequest(validators.EMPTY_PASSWORD)
    
    if len(password) < 8:
        raise BadRequest(validators.INVALID_PASSWORD)
    
    if not (any(c.isupper() for c in password) and 
            any(c.islower() for c in password) and 
            any(c.isdigit() for c in password) and 
            any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password)):
        raise BadRequest(validators.UNCOMPLEX_PASSWORD)
    
    validateFirstName(data)
    validateLastName(data)
    
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")

    
    if first_name.lower() in password.lower():
        raise BadRequest(validators.FIRST_NAME_IN_PASSWORD)
    
    if last_name.lower() in password.lower():
        raise BadRequest(validators.LAST_NAME_IN_PASSWORD)
    
    # Check for unaccepted characters
    if any(c.isspace() or c in "\"'`" for c in password):
        raise BadRequest(validators.UNACCEPTED_CHARACTERS_IN_PASSWORD)


def validateFirstName(data):
    first_name = data.get("first_name")
    
    if first_name is None:
        raise BadRequest(validators.MISSING_FIRST_NAME)
    
    if not first_name.strip():
        raise BadRequest(validators.EMPTY_FIRST_NAME)


def validateLastName(data):
    last_name = data.get("last_name")
    if last_name is None:
        raise BadRequest(validators.MISSING_LAST_NAME)
    if not last_name.strip():
        raise BadRequest(validators.EMPTY_LAST_NAME)


def validateEmail(data):
    email = data.get("email")
    
    if email is None:
        raise BadRequest(validators.MISSING_EMAIL)
    
    if not email.strip():
        raise BadRequest(validators.EMPTY_EMAIL)
    
    try:
        validate_email(email)
    except ValidationError:
        raise BadRequest(validators.INVALID_EMAIL)
    
    if User.objects.filter(email=email).exists():
        raise BadRequest(validators.TAKEN_EMAIL)
    

def validateDateOfBirth(data):
    date_of_birth = data.get("date_of_birth")
    
    if date_of_birth is None:
        raise BadRequest(validators.MISSING_DATE_OF_BIRTH)
    
    if not date_of_birth.strip():
        raise BadRequest(validators.EMPTY_DATE_OF_BIRTH)
    
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    except BadRequest:
        raise BadRequest(validators.INVALID_DATE_OF_BIRTH)
    
    if dob > datetime.now().date():
        raise BadRequest(validators.FUTURE_DATE_OF_BIRTH)
    
    if (datetime.now().date() - dob).days > 36525:  # 100 years
        raise BadRequest(validators.OLD_DATE_OF_BIRTH)

def validatePhoneNumber(data):
    phone_number = data.get("phone_number")
    
    if phone_number is None:
        raise BadRequest(validators.MISSING_PHONE_NUMBER)
    
    if not phone_number.strip():
        raise BadRequest(validators.EMPTY_PHONE_NUMBER)
    
    phone_validator = RegexValidator(r"^\+?[1-9]\d{1,14}$", validators.INVALID_PHONE_NUMBER)
    try:
        phone_validator(phone_number)
    except ValidationError:
        raise BadRequest(validators.INVALID_PHONE_NUMBER)
    
    if User.objects.filter(phone_number=phone_number).exists():
        raise BadRequest(validators.TAKEN_PHONE_NUMBER)


def validateWeight(data):
    weight = data.get("weight")
    
    if weight is None:
        raise BadRequest(validators.MISSING_WEIGHT)
    
    if not weight.strip():
        raise BadRequest(validators.EMPTY_WEIGHT)
    
    try:
        weight_value = float(weight)
    except BadRequest:
        raise BadRequest(validators.INVALID_WEIGHT)
    
    if weight_value < 0:
        raise BadRequest(validators.SMALL_WEIGHT)
    
    if weight_value > 500:
        raise BadRequest(validators.LARGE_WEIGHT)


def validateHeight(data):
    height = data.get("height")
    
    if height is None:
        raise BadRequest(validators.MISSING_HEIGHT)
    
    if not height.strip():
        raise BadRequest(validators.EMPTY_HEIGHT)
    
    try:
        height_value = int(height)
    except BadRequest:
        raise BadRequest(validators.INVALID_HEIGHT)
    
    if height_value < 40:
        raise BadRequest(validators.SMALL_HEIGHT)
    
    if height_value > 300:
        raise BadRequest(validators.LARGE_HEIGHT)