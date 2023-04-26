from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    registered_hackathon = models.CharField(max_length=100, default='.')
    is_super_user = models.BooleanField(default='false')

    def __str__(self):
        return self.user.username
