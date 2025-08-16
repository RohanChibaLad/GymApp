from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from UserApp.viewHandling.userViews import userRegister, userLogin, userLogout, userDelete

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
        userGet(request)
    elif request.method == "DELETE":
        userDelete(request)

    return HttpResponse(
        content="Method not allowed",
        content_type="text/plain",
        status=400
    )

def login(request):
    """
    A view to handle user login.
    """
    if request.method == 'POST':
        return userLogin(request)
    
    return HttpResponse(
        content="Method not allowed",
        content_type="text/plain",
        status=401)
    
def logout(request):
    """
    A view to handle user logout.
    """
    if request.method == 'POST':
        return userLogout(request)
    
    return HttpResponse(
        content="Method not allowed",
        content_type="text/plain",
        status=401)

