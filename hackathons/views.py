from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import Hackathon
from .serializers import HackathonSerializer
from users.serializers import ProfileSerializer
from users.models import Profile
from submissions.models import Submission


@login_required()
@api_view(['GET'])
def index(request):
    cur_user = request.user.username
    return Response({
        "username": cur_user,
        "message": "You are in hackathons portal."
    })


# Below function is used to post a new hackathon. Only superusers are allowed to post a hackathon.
# If the logged-in user is a superuser then he is allowed to post a hackathon, else not.
@login_required()
@api_view(['POST'])
def post_hackathon(request):
    if request.user.is_superuser:
        user = request.user.username
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if Hackathon.objects.filter(title=title).exists():
            return Response({"message": "Hackathon with this name already exists. Choose another name."})
        else:
            new_hackathon = Hackathon.objects.create(
                user=user, title=title, description=description,
                start_time=start_time, end_time=end_time, created_by=request.user.username)

            serializer = HackathonSerializer(new_hackathon)

            if not serializer.is_valid():
                return Response({"payload": serializer.errors, "message": "An error occurred"})

            serializer.save()
            return Response({
                "payload": serializer.data,
                "message": "Hackathon posted successfully."
            })
    else:
        return Response({"message": "You have to be a superuser to post a hackathon."})


# Get the JSON response containing all the posted hackathons.
@login_required()
@api_view(['GET'])
def get_hackathons(request):
    all_hackathons = Hackathon.objects.all()

    serializer = HackathonSerializer(all_hackathons)
    if not serializer.is_valid():
        return Response({
            "payload": serializer.errors,
            "message": "An error occurred"
        })

    return Response({
        "payload": serializer.data,
        "message": "Fetch successful"
    })


# Below function is used to registering a user for a hackathon.
# The user provides the title of the hackathon that he wants to register in.
# User can only be registered into one hackathon at a time.
@login_required()
@api_view(['POST'])
def register_for_hackathon(request):
    hackathon_title = request.POST.get('hackathon_title')
    user = request.user.username

    if Profile.objects.get(id_user=request.user.id).registered_hackathon is not '.':
        return Response({
            "hackathon_title": hackathon_title,
            "user": user,
            "message": "You are already registered."
        })
    else:
        if Hackathon.objects.filter(title=hackathon_title).exists():
            cur_user = Profile.objects.get(id_user=request.user.id)
            cur_user.registered_hackathon = hackathon_title

            serializer = ProfileSerializer(cur_user)
            if not serializer.is_valid():
                return Response({
                    "payload": serializer.errors,
                    "message": "An error occurred."
                })

            cur_user.save()

            return Response({
                "payload": serializer.data,
                "message": "Registered successfully."
            })
        else:
            return Response({
                "message": "The hackathon of the provided title does not exist."
            })


# Below function is used to delete a posted hackathon. It can be deleted only by a superuser.
@login_required()
@api_view(['POST'])
def delete_hackathon(request):
    if request.user.is_superuser:
        hackathon_title = request.POST.get('hackathon_title')

        if Hackathon.objects.filter(title=hackathon_title).exists():
            my_hackathon = Hackathon.objects.get(title=hackathon_title)
            cur_user = Profile.objects.get(user=request.user)
            all_submissions = Submission.objects.all()
            cur_user.registered_hackathon = '.'
            cur_user.save()
            all_submissions.delete()
            my_hackathon.delete()

            return Response({
                "hackathon_title": hackathon_title,
                "created_by": request.user.username,
                "message": "Hackathon deleted successfully."
            })
        else:
            return Response({
                "message": "This hackathon does not exist."
            })

    else:
        return Response({
            "message": "You have to be a superuser to delete a posted hackathon."
        })
