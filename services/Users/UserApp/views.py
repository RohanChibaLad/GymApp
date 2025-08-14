from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

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
    
    firstName = data.get("first_name")
    lastName = data.get("last_name")
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    height = data.get("height")
    weight = data.get("weight")
    dateOfBirth = data.get("date_of_birth")
    phoneNumber = data.get("phone_number")
    
    
    return JsonResponse(
    {
        "ok": True,
        "received": {
            "firstName": firstName,
            "lastName": lastName,
            "username": username,
            "password": password,
            "email": email,
            "height": height,
            "weight": weight,
            "dateOfBirth": dateOfBirth,
            "phoneNumber": phoneNumber
        }
    },
    status=201,
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