from UserApp.models import User  # Importing the custom User model 
from django.core.exceptions import ValidationError, BadRequest, ObjectDoesNotExist
from django.core.validators import validate_email, RegexValidator
from decimal import Decimal, InvalidOperation


from UserApp.viewHandling import viewHandlingConstants as validators  # Importing validation messages
from datetime import datetime

def validateUsername(username: str) -> str:
    if username is None:
        raise BadRequest(validators.MISSING_USERNAME)
    
    if not isinstance(username, str):
        raise BadRequest(validators.INVALID_USERNAME_TYPE)
    
    username = username.strip()
    if not username:
        raise BadRequest(validators.EMPTY_USERNAME)

    return username

def validateGetUsername(data):
    """
    Validates the username field in the provided data.
    """
    username = data.get("username")
    
    u_username = validateUsername(username)  # Check if username is provided and not empty
    validateUsernameExists(u_username)  # Check if username exists in the database

def validateUniqueUsername(username: str) -> None:
    if User.objects.filter(username=username).exists():
        raise BadRequest(validators.TAKEN_USERNAME)

def validateUsernameLength(username):
    if len(username) < 3 or len(username) > 150:
        raise BadRequest(validators.INVALID_USERNAME)
    
def validateCreateUsername(data: dict) -> str:
    username = data.get("username")
    
    validateUsername(username)  # Check if username is provided and not empty
    validateUniqueUsername(username)  # Check if username is unique
    validateUsernameLength(username)  # Check if username length is valid
    
    return username

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

    return password

def validatePassword(password: str) -> str:
    if password is None:
        raise BadRequest(validators.MISSING_PASSWORD)

    if not isinstance(password, str):
        raise BadRequest(validators.INVALID_PASSWORD_TYPE)

    password = password.strip()
    if not password:
        raise BadRequest(validators.EMPTY_PASSWORD)
    
    return password
    
def validateFirstName(data: dict) -> str:
    first_name = data.get("first_name")
    
    if first_name is None:
        raise BadRequest(validators.MISSING_FIRST_NAME)
    
    if not isinstance(first_name, str):
        raise BadRequest(validators.INVALID_FIRST_NAME_TYPE)

    first_name = first_name.strip()
    if not first_name:
        raise BadRequest(validators.EMPTY_FIRST_NAME)

    return first_name

def validateLastName(data: dict) -> str:
    last_name = data.get("last_name")
    if last_name is None:
        raise BadRequest(validators.MISSING_LAST_NAME)
    
    if not isinstance(last_name, str):
        raise BadRequest(validators.INVALID_LAST_NAME_TYPE)
    
    last_name = last_name.strip()
    if not last_name:
        raise BadRequest(validators.EMPTY_LAST_NAME)

    return last_name

def validateEmail(email: str) -> str:
    if email is None:
        raise BadRequest(validators.MISSING_EMAIL)
    
    if not isinstance(email, str):
        raise BadRequest(validators.INVALID_EMAIL_TYPE)
    
    email = email.strip().lower()
    if not email:
        raise BadRequest(validators.EMPTY_EMAIL)
    
    try:
        validate_email(email)
    except ValidationError:
        raise BadRequest(validators.INVALID_EMAIL)
    
    return email
    
def validateGetEmail(data):
    email = data.get("email")
    
    u_email = validateEmail(email)  # Validate email format
    validateEmailExists(u_email)  # Check if email exists in the database

def validateUniqueEmail(email: str) -> None:
    if User.objects.filter(email=email).exists():
        raise BadRequest(validators.TAKEN_EMAIL)

def validateCreateEmail(data: dict) -> str:
    email = data.get("email")
    validateEmail(email)  # Validate email format
    validateUniqueEmail(email)  # Check if email is unique 
    return email

def validateEmailExists(email):
    
    if not User.objects.filter(email=email).exists():
        raise ObjectDoesNotExist(validators.EMAIL_DOES_NOT_EXIST)

def validateDateOfBirth(data: dict):
    dob_str = data.get("date_of_birth")
    if dob_str is None:
        raise BadRequest(validators.MISSING_DATE_OF_BIRTH)
    
    if not isinstance(dob_str, str):
        raise BadRequest(validators.INVALID_DATE_OF_BIRTH)
    
    dob_str = dob_str.strip()
    if not dob_str:
        raise BadRequest(validators.EMPTY_DATE_OF_BIRTH)
    
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        raise BadRequest(validators.INVALID_DATE_OF_BIRTH)
    
    today = datetime.now().date()
    if dob > today:
        raise BadRequest(validators.FUTURE_DATE_OF_BIRTH)
    
    if (today - dob).days > 36525:
        raise BadRequest(validators.OLD_DATE_OF_BIRTH)
    
    return dob

def validatePhoneNumber(data: dict) -> str:
    phone = data.get("phone_number")
    
    if phone is None:
        raise BadRequest(validators.MISSING_PHONE_NUMBER)
    
    if not isinstance(phone, str):
        raise BadRequest(validators.INVALID_PHONE_NUMBER_TYPE)
    
    phone = phone.strip()
    if not phone:
        raise BadRequest(validators.EMPTY_PHONE_NUMBER)
    
    phone_validator = RegexValidator(r"^\+?[1-9]\d{1,14}$", validators.INVALID_PHONE_NUMBER)
    try:
        phone_validator(phone)
    except ValidationError:
        raise BadRequest(validators.INVALID_PHONE_NUMBER)
    
    validateUniquePhoneNumber(phone)
    
    return phone

def validateUniquePhoneNumber(phone_number):
    if User.objects.filter(phone_number=phone_number).exists():
        raise BadRequest(validators.TAKEN_PHONE_NUMBER)

def validateWeight(data: dict) -> Decimal:
    weight = data.get("weight")
    
    if weight is None:
        raise BadRequest(validators.MISSING_WEIGHT)
    
    try:
        w = Decimal(str(weight))  # robust to int/float/str
    except (InvalidOperation, TypeError):
        raise BadRequest(validators.INVALID_WEIGHT)
    
    if w < 0:
        raise BadRequest(validators.SMALL_WEIGHT)
    
    if w > Decimal("500"):
        raise BadRequest(validators.LARGE_WEIGHT)
    
    w = w.quantize(Decimal("0.01"))
    return w


def validateHeight(data: dict) -> int:
    height = data.get("height")
    
    if height is None:
        raise BadRequest(validators.MISSING_HEIGHT)
    
    try:
        h = int(height)
    except (ValueError, TypeError):
        raise BadRequest(validators.INVALID_HEIGHT)
    
    if h < 40:
        raise BadRequest(validators.SMALL_HEIGHT)
    
    if h > 300:
        raise BadRequest(validators.LARGE_HEIGHT)
    
    return h

def validateUserID(user_id) -> int:
    if user_id is None:
        raise BadRequest(validators.MISSING_USER_ID)
    
    if isinstance(user_id, str) and not user_id.strip():
        raise BadRequest(validators.EMPTY_USER_ID)
    
    try:
        uid = int(user_id)
    except (ValueError, TypeError):
        raise BadRequest("User ID must be an integer.")
    
    if uid <= 0:
        raise BadRequest(validators.INVALID_USER_ID_VALUE)
    
    return uid

def validateUserIDExists(user_id: int) -> None:
    if not User.objects.filter(id=user_id).exists():
        raise ObjectDoesNotExist(validators.ID_DOES_NOT_EXIST)

def validateGetUserID(data):
    user_id = data.get("id")
    
    uid = validateUserID(user_id)  # Validate user ID format
    validateUserIDExists(uid)

def validateLoginData(data):
    username = data.get("username")
    password = data.get("password")
    
    validateUsername(username)  # Check if username is provided and not empty
    validatePassword(password)  # Check if password is provided and not empty

def validateGetStudentData(data: dict) -> None:
    if "id" in data:
        validateGetUserID(data)
    elif "username" in data:
        validateGetUsername(data)
    elif "email" in data:
        validateGetEmail(data)
    else:
        raise BadRequest("At least one of 'id', 'username', or 'email' must be provided.")
    
def validateDeleteStudentData(data: dict) -> None:
    if "id" in data:
        validateGetUserID(data)
    else:
        raise BadRequest(validators.MISSING_USER_ID)
    