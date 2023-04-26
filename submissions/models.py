import datetime
from django.db import models
import uuid


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    submission_name = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    hackathon_title = models.CharField(max_length=100)
    github_link = models.CharField(max_length=200)
    created_by = models.CharField(max_length=100)
    submission_time = models.DateTimeField()
