import json

from UserApp.models import User  # Importing the custom User model 
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import BadRequest

from UserApp.viewHandling.viewHandlingValidators import validateUsername, validatePassword  # Importing the validation function

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
        validatePassword(data)  # Validating password
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
    
    
    return JsonResponse({"User Created!": True, "User ID": user.id, "Name": user.first_name}, status=201,
)

def userLogin(request):
    """
    A view to handle user login.
    """
    # Logic for user login
    pass    
    
def userDelete(request):
    """
    A view to handle user deletion.
    """
    # Logic for user deletion
    pass