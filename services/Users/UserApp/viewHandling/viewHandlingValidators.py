from UserApp.models import User  # Importing the custom User model 
from django.core.exceptions import ValidationError, BadRequest, ObjectDoesNotExist
from django.core.validators import validate_email, RegexValidator

from UserApp.viewHandling import viewHandlingConstants as validators  # Importing validation messages
from datetime import datetime

def validateUsername(username):
    if username is None:
        raise BadRequest(validators.MISSING_USERNAME)
    
    if not username.strip():
        raise BadRequest(validators.EMPTY_USERNAME)
    
    if not isinstance(username, str):
        raise BadRequest(validators.INVALID_USERNAME_TYPE)

def validateGetUsername(data):
    """
    Validates the username field in the provided data.
    """
    username = data.get("username")
    
    validateUsername(username)  # Check if username is provided and not empty
    validateUsernameExists(username)  # Check if username exists in the database

def validateUniqueUsername(username):
    if User.objects.filter(username=username).exists():
        raise BadRequest(validators.TAKEN_USERNAME)

def validateUsernameLength(username):
    if len(username) < 3 or len(username) > 150:
        raise BadRequest(validators.INVALID_USERNAME)
    
def validateCreateUsername(data):
    """
    Validates the username field in the provided data.
    """
    username = data.get("username")
    
    validateUsername(username)  # Check if username is provided and not empty
    validateUniqueUsername(username)  # Check if username is unique
    validateUsernameLength(username)  # Check if username length is valid

def validateUsernameExists(username):
    """
    Checks if a user with the given username exists in the database.
    """
    if not User.objects.filter(username=username).exists():
        raise ObjectDoesNotExist(validators.USERNAME_DOES_NOT_EXIST)

def validateCreatePassword(data):
    """
    Validates the password field in the provided data.
    """
    password = data.get("password")
    
    validatePassword(password)
    
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

def validatePassword(password):
    if password is None:
        raise BadRequest(validators.MISSING_PASSWORD)
    
    if not password.strip():
        raise BadRequest(validators.EMPTY_PASSWORD)

    if not isinstance(password, str):
        raise BadRequest(validators.INVALID_PASSWORD_TYPE)
    
def validateFirstName(data):
    first_name = data.get("first_name")
    
    if first_name is None:
        raise BadRequest(validators.MISSING_FIRST_NAME)
    
    if not first_name.strip():
        raise BadRequest(validators.EMPTY_FIRST_NAME)
    
    if not isinstance(first_name, str):
        raise BadRequest(validators.INVALID_FIRST_NAME_TYPE)


def validateLastName(data):
    last_name = data.get("last_name")
    if last_name is None:
        raise BadRequest(validators.MISSING_LAST_NAME)
    if not last_name.strip():
        raise BadRequest(validators.EMPTY_LAST_NAME)
    
    if not isinstance(last_name, str):
        raise BadRequest(validators.INVALID_LAST_NAME_TYPE)

def validateEmail(email):
    
    if email is None:
        raise BadRequest(validators.MISSING_EMAIL)
    
    if not email.strip():
        raise BadRequest(validators.EMPTY_EMAIL)
    
    try:
        validate_email(email)
    except ValidationError as e:
        raise BadRequest(validators.INVALID_EMAIL)
    
    if not isinstance(email, str):
        raise BadRequest(validators.INVALID_EMAIL_TYPE)
    
def validateGetEmail(data):
    """
    Validates the email field in the provided data.
    """
    email = data.get("email")
    
    validateEmail(email)  # Validate email format
    validateEmailExists(email)  # Check if email exists in the database

def validateUniqueEmail(email):
    if User.objects.filter(email=email).exists():
        raise BadRequest(validators.TAKEN_EMAIL)

def validateCreateEmail(data):
    email = data.get("email")
    validateEmail(email)  # Validate email format
    validateUniqueEmail(email)  # Check if email is unique 

def validateEmailExists(email):
    
    if not User.objects.filter(email=email).exists():
        raise ObjectDoesNotExist(validators.EMAIL_DOES_NOT_EXIST)

def validateDateOfBirth(data):
    date_of_birth = data.get("date_of_birth")
    
    if date_of_birth is None:
        raise BadRequest(validators.MISSING_DATE_OF_BIRTH)
    
    if not date_of_birth.strip():
        raise BadRequest(validators.EMPTY_DATE_OF_BIRTH)
    
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    except ValueError:
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
    
    validateUniquePhoneNumber(phone_number)  # Check if phone number is unique
    
    if not isinstance(phone_number, str):
        raise BadRequest(validators.INVALID_PHONE_NUMBER_TYPE)

def validateUniquePhoneNumber(phone_number):
    if User.objects.filter(phone_number=phone_number).exists():
        raise BadRequest(validators.TAKEN_PHONE_NUMBER)

def validateWeight(data):
    weight = data.get("weight")
    
    if weight is None:
        raise BadRequest(validators.MISSING_WEIGHT)
    
    if not str(weight).strip():
        raise BadRequest(validators.EMPTY_WEIGHT)
    
    try:
        weight_value = float(weight)
    except BadRequest:
        raise BadRequest(validators.INVALID_WEIGHT)
    
    if weight_value < 0:
        raise BadRequest(validators.SMALL_WEIGHT)
    
    if weight_value > 500:
        raise BadRequest(validators.LARGE_WEIGHT)

    if not isinstance(weight, (int, float)):
        raise BadRequest(validators.INVALID_WEIGHT_TYPE)

def validateHeight(data):
    
    height = data.get("height")
    
    if height is None:
        raise BadRequest(validators.MISSING_HEIGHT)
    
    if not str(height).strip():
        raise BadRequest(validators.EMPTY_HEIGHT)
    
    try:
        height_value = int(height)
    except BadRequest:
        raise BadRequest(validators.INVALID_HEIGHT)
    
    if height_value < 40:
        raise BadRequest(validators.SMALL_HEIGHT)
    
    if height_value > 300:
        raise BadRequest(validators.LARGE_HEIGHT)
    
    if not isinstance(height, int):
        raise BadRequest(validators.INVALID_HEIGHT_TYPE)

def validateUserID(user_id):
    if not user_id.strip():
        raise BadRequest(validators.EMPTY_USER_ID)
    try:
        user_id = int(user_id)              
    except (ValueError, TypeError):
        raise BadRequest("User ID must be an integer.")
    
    
    if user_id is None:
        raise BadRequest(validators.MISSING_USER_ID)
    
    if user_id <= 0:
        raise BadRequest(validators.INVALID_USER_ID_VALUE)

def validateGetUserID(data):
    """
    Validates the user ID field in the provided data.
    """
    user_id = data.get("id")
    
    validateUserID(user_id)  # Validate user ID format
    validateUserIDExists(user_id)

def validateUserIDExists(user_id):
    """
    Checks if a user with the given ID exists in the database.
    """
    if not User.objects.filter(id=user_id).exists():
        raise ObjectDoesNotExist(validators.ID_DOES_NOT_EXIST)

def validateLoginData(data):
    """
    Validates the login data provided in the request.
    """
    username = data.get("username")
    password = data.get("password")
    
    validateUsername(username)  # Check if username is provided and not empty
    validatePassword(password)  # Check if password is provided and not empty

def validateGetStudentData(data: dict) -> None:
    try:
        if "id" in data:
            validateGetUserID(data)
        elif "username" in data:
            validateGetUsername(data)
        else:
            validateGetEmail(data)
    except ValidationError as e:
        raise ObjectDoesNotExist(str(e))
    
def validateDeleteStudentData(data: dict) -> None:
    """
    Validates the data for deleting a user.
    """
    if "id" in data:
        validateGetUserID(data)
    else:
        raise BadRequest(validators.MISSING_USER_ID)
    