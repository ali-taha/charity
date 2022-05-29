from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ChoiceField

User = get_user_model()

CHOICE_EXPERIENCE = [
    (0,'Beginner'),
    (1,'Intermediate'),
    (2,'Expert'),
]


class Benefactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=CHOICE_EXPERIENCE, default=0)
    free_time_per_week = models.PositiveIntegerField(default=0)

class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

GENDER_CHOICES = [
        ('M','Man'),
        ('F','Female'),
    ]

STATE_CHOICES = [
    ('P','Pending'),
    ('W','Waiting'),
    ('A','Assigned'),
    ('D','Done'),
]


class Task(models.Model):
    assigned_benefactor = models.ForeignKey(Benefactor, null=True, on_delete=models.SET_NULL)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    age_limit_from = models.IntegerField(null=True, blank=True)
    age_limit_to = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)