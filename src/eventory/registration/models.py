from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    interests = models.JSONField(null=True)

    def __str__(self):
        return self.email


class Interest(models.Model):
    interest = models.CharField(max_length=25)

    def __str__(self):
        return self.interest


class Event(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.title
