from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    category = models.TextField()
    question = models.TextField()
    value = models.FloatField()

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.FloatField(default=0)