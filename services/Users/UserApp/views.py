from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from UserApp.models import User  # Importing the custom User model 
import json

# Create your views here.
@ensure_csrf_cookie
def get_CSRF_token(request):
    """
    A view to return the CSRF token for AJAX requests.
    """
    return JsonResponse({'csrfToken': get_token(request)})

def user(request):
    """
    A view to handle user functions.
    """
    if request.method == 'POST':
        return userRegister(request)
    elif request.method == 'GET':
        userLogin(request)
    elif request.method == "DELETE":
        userDelete(request)
    
    # Render a template for user actions
    return render(request, 'register.html')


def userRegister(request):
    """
    A view to handle user registration.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
        
    except ValueError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    
    #Validate required fields - TO DO
    
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
    
    
    return JsonResponse({"User Created!": True}, status=201,
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