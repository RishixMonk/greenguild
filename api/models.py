from django.db import models

# Create your models here.
class Question(models.Model):
    category = models.TextField()
    question = models.TextField()
    value = models.FloatField()

class User(models.Model):
    name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    score = models.FloatField()