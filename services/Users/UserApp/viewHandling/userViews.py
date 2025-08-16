import json

from UserApp.models import User  # Importing the custom User model 
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import BadRequest
from django.contrib.auth import authenticate, login, logout

from UserApp.viewHandling.viewHandlingValidators import validateUsername, validatePassword, validateEmail, validateDateOfBirth, validatePhoneNumber, validateHeight, validateWeight, validateLoginData  # Importing the validation function

def userRegister(request):
    """
    A view to handle user registration.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    
    #Validate required fields - TO DO
    try:
        validateUsername(data) # Validating user data
        validatePassword(data)  # Validating password --> also validate first and last name
        validateEmail(data)       # Validating email
        validateDateOfBirth(data) # Validating date of birth
        validatePhoneNumber(data)  # Validating phone number
        validateWeight(data)       # Validating weight
        validateHeight(data)       # Validating height
        
    except BadRequest as e: # Catching validation errors
        return HttpResponse(
            content=str(e),
            content_type="Validation Error",
            status=400)
    
    #Add user to database
    user = User.objects.create_user(
        username=data.get("username"),
        password=data.get("password"), 
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        date_of_birth=data.get("date_of_birth"),
        phone_number=data.get("phone_number"),
        weight=data.get("weight"),
        height=data.get("height")
    )
    
    
    return JsonResponse({"User Created!": True, "User ID": user.id, "Name": user.first_name}, status=201,)

def userLogin(request):
    """
    A view to handle user login.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    try:    
        validateLoginData(data)
    except BadRequest as e:
        return HttpResponse(
            content=str(e),
            content_type="Validation Error",
            status=400)
    
    #Check if user exists
    if not authenticateUser(request, data):
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    response = createUserResponseData(request.user)
    response["message"] = "User logged in successfully"
    return JsonResponse(response, status=200)
    
def userLogout(request):
    """
    A view to handle user logout.
    """
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "User logged out successfully"}, status=200)
    return HttpResponse(
        content="User not logged in",
        content_type="text/plain",
        status=401
    )
    

def authenticateUser(request, requestData: dict):
    """
    A function to authenticate the user.
    """
    user = authenticate(username=requestData["username"], password=requestData["password"])
    if user is not None:
        login(request, user)
        return True
    return False

def createUserResponseData(user: User) -> dict:
    """
    A function to create a response data dictionary for the user.
    """
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
        "phone_number": user.phone_number,
        "weight": str(user.weight) if user.weight is not None else None,
        "height": user.height
    }
    
def userDelete(request):
    """
    A view to handle user deletion.
    """
    # Logic for user deletion
    pass