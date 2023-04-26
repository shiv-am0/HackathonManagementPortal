import datetime
import pytz
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import Submission
from users.models import Profile
from rest_framework.response import Response
from .serializers import SubmissionSerializer


@login_required()
@api_view(['GET'])
def index(request):
    cur_user = request.user.username
    return Response({
        "username": cur_user,
        "message": "You are in submissions portal."
    })


# Function to get all submissions to a particular hackathon. Submissions can only be viewed by superusers.
# Submissions can be viewed from newest to oldest and vice versa by passing ASC/DESC in sort_by field.
@login_required()
@api_view(['POST'])
def get_all_submissions(request):
    if request.user.is_superuser:
        hackathon_title = request.POST.get('hackathon_title')
        sort_by = request.POST.get('sort_by')
        print(hackathon_title)
        all_submissions = Submission.objects.all()
        print(all_submissions)
        res = []

        if sort_by == 'ASC':
            all_submissions = all_submissions.order_by('submission_time')
        elif sort_by == 'DESC':
            all_submissions = all_submissions.order_by('-submission_time')
        else:
            return Response({
                "message": "Please enter a valid sort_by command, i.e. ASC/DESC"
            })

        found = False
        for sub in all_submissions:
            if sub.hackathon_title == str(hackathon_title):
                found = True
                res.append(sub)

        if found is True:
            serializer = SubmissionSerializer(res)
            print(f'Data = {serializer.data}')
            return Response(serializer.data)
        else:
            return Response({
                "message": "There are no submissions."
            })
    else:
        return Response({
            "message": "You have to be a superuser to view the submissions."
        })


# Below function is used to make a submission to the registered hackathon by the user.
@login_required()
@api_view(['POST'])
def make_submission(request):
    submission_name = request.POST.get('submission_name')
    summary = request.POST.get('summary')
    hackathon_title = request.POST.get('hackathon_title')
    github_link = request.POST.get('github_link')
    created_by = request.user.username

    if Profile.objects.get(id_user=request.user.id).registered_hackathon != hackathon_title:
        return Response({
            "message": "Yor are not registered for this hackathon."
        })
    elif Profile.objects.get(id_user=request.user.id).registered_hackathon == hackathon_title and \
            Submission.objects.filter(created_by=created_by).exists():
        return Response({
            "username": request.user.username,
            "created_by": created_by,
            "hackathon_title": hackathon_title,
            "message": "You have already submitted your submission."
        })
    else:
        new_submission = Submission.objects.create(
            submission_name=submission_name,
            summary=summary,
            hackathon_title=hackathon_title,
            github_link=github_link,
            created_by=created_by,
            submission_time=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        )

        serializer = SubmissionSerializer(new_submission)
        if not serializer.is_valid():
            return Response({
                "payload": serializer.errors,
                "message": "An error occurred."
            })

        serializer.save()
        return Response({
            "payload": serializer.data,
            "message": "Submission uploaded successfully."
        })


# Delete a submission based on its submission name and hackathon title.
@login_required()
@api_view(['POST'])
def delete_submission(request):
    submission_name = request.POST.get('submission_name')
    hackathon_title = request.POST.get('hackathon_title')
    created_by = request.user.username

    if Submission.objects.filter(submission_name=submission_name, hackathon_title=hackathon_title,
                                 created_by=created_by).exists():
        my_submission = Submission.objects.get(submission_name=submission_name, hackathon_title=hackathon_title,
                                               created_by=created_by)

        serializer = SubmissionSerializer(my_submission)
        if not serializer.is_valid():
            return Response({
                "payload": serializer.errors,
                "message": "An error occurred."
            })

        my_submission.delete()

        return Response({
            "payload": serializer.data,
            "message": "Submission deleted successfully."
        })
    else:
        return Response({
            "message": "This submission can not be deleted."
        })
