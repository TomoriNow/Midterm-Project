from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Successful login status.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
                # Add other data if you want to send data to Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account disabled."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, check email or password again."
        }, status=401)
    
@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout failed."
        }, status=401)
    
@csrf_exempt
def register(request):
    username = request.POST['username']
    password = request.POST['password']
    
    # Check if the username is already taken
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "status": False,
            "message": "Username is already taken."
        }, status=400)
    
    # Check if username and password are provided
    if not username or not password:
        return JsonResponse({
            "status": False,
            "message": "Username and password are required for registration."
        }, status=400)

    
    
    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Registered successfully!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Register failed, please try again."
        }, status=401)