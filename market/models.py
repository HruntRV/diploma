from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar')
    phone = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return self.user.username

