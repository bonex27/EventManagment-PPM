from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    participants = models.ManyToManyField(User, related_name="participants")

    def __str__(self):
        return self.name
