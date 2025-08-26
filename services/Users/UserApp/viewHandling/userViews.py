import json

from UserApp.models import User  # Importing the custom User model 
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import BadRequest, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout

from UserApp.viewHandling.viewHandlingValidators import validateCreateUsername, validateCreatePassword, validateCreateEmail, validateDateOfBirth, validatePhoneNumber, validateWeight, validateHeight, validateLoginData, validateGetStudentData, validateDeleteStudentData

def userRegister(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        username = validateCreateUsername(data)
        password = validateCreatePassword(data)
        email = validateCreateEmail(data)
        dob = validateDateOfBirth(data)            # returns date (if you return it)
        phone = validatePhoneNumber(data)
        weight = validateWeight(data)
        height = validateHeight(data)
    except BadRequest as e:
        return JsonResponse({"error": str(e)}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=email,
        date_of_birth=dob,          
        phone_number=phone,
        weight=weight,
        height=height,
    )
    return JsonResponse({"ok": True, "id": user.id, "name": user.first_name}, status=201)

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

def userGet(request):
    data = request.GET.dict()
    if not data:
        return userGetSelf(request)

    try:
        validateGetStudentData(data)
        if "id" in data:
            user = User.objects.get(id=data["id"])
        elif "username" in data:
            user = User.objects.get(username=data["username"])
        else:
            user = User.objects.get(email=data["email"])
    except BadRequest as e:
        return JsonResponse({"error": str(e)}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    userResponse = createUserResponseData(user)
    userResponse["message"] = "User data retrieved successfully"
    
    return JsonResponse(data, status=200)

def userGetSelf(request):
    """
    A view to handle retrieval of the authenticated user's data.
    """
    if not request.user.is_authenticated:
        return HttpResponse(
            content="User not logged in",
            content_type="text/plain",
            status=401
        )
    
    user = request.user
    returnData = createUserResponseData(user)
    returnData["message"] = "User data retrieved successfully"
    return JsonResponse(returnData, status=200)
    
def userDelete(request):
    data = request.GET.dict()

    try:
        raw = (request.body or b"").decode("utf-8")
        if raw.strip():
            body = json.loads(raw)
            if isinstance(body, dict):
                data.update(body)
            else:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        validateDeleteStudentData(data)
    except BadRequest as e:
        return JsonResponse({"error": str(e)}, status=400)

    try:
        user = User.objects.get(id=data["id"])
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    user.delete()
    return JsonResponse({"message": "User deleted successfully"}, status=200)
