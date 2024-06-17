import datetime

from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    max_participants = models.IntegerField(default=100)
    participants = models.ManyToManyField(User, related_name="participants")

    def __str__(self):
        return self.name
