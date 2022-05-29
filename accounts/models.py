from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ChoiceField


GENDER_CHOICES = [
    ('M','Man'),
    ('F','Female'),
]

class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)