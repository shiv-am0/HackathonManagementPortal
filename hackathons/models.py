from django.db import models
import uuid
from datetime import datetime


class Hackathon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return self.user

