from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Profile
from .serializers import ProfileSerializer


# Below function is used to get the object of currently logged-in user and use that to get the user profile
@login_required()
@api_view(['GET'])
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    return Response({
        "username": user_profile.user.username,
        "message": "User logged in"
    })


@api_view(['GET'])
def get_registered_users(request):
    my_hackathons = []
    for p in Profile.objects.raw("SELECT * FROM users_profile WHERE is_registered != '.' "):
        my_hackathons.append(p)
        return Response({
            "payload": my_hackathons
        })


@api_view(['POST'])
def signup(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    is_super_user = request.POST.get('isSuperUser')
    print(is_super_user)

    # Proceed if the entered password matches with the conform password
    if password == password2:
        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already exists"})
        elif User.objects.filter(username=username).exists():
            return Response({"message": "Username already exists"})
        else:
            if is_super_user == 'true':
                print("Creating superuser")
                user = User.objects.create_superuser(username=username, email=email, password=password)
            else:
                print("Creating normal user")
                user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Log user in after registering
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            # Create a Profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(
                user=user_model,
                id_user=user_model.id,
                is_super_user=user_model.is_superuser
            )

            serializer = ProfileSerializer(data=new_profile)

            if not serializer.is_valid():
                return Response({"payload": serializer.errors, "message": "An error occurred."})

            serializer.save()

            return Response({
                "payload": serializer.data,
                "message": "Signup successful."
            })
    else:
        return Response({
            "username": username,
            "email": email,
            "message": "Passwords do not match. Please try again."
        })


# Below function is used to authenticate a current user profile
@api_view(['POST'])
def signin(request):
    username = request.get('username')
    password = request.get('password')

    user = auth.authenticate(username=username, password=password)

    # If the credentials match from the auth DB, then login
    if user is not None:
        auth.login(request, user)
        return Response({
            "username": username,
            "message": "Signin successful"
        })
    else:
        return Response({
            "message": "Invalid credentials"
        })


# Below function is used to logout the current user
@login_required()
@api_view(['GET'])
def logout(request):
    auth.logout(request)
    return Response({
        "message": "Logout successful"
    })
