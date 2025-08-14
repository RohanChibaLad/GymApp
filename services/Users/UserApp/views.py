from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from UserApp.viewHandling.userViews import userRegister, userLogin, userDelete

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


