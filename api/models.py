from django.db import models

# Create your models here.
class Question(models.Model):
    category = models.TextField()
    question = models.TextField()
    value = models.FloatField()

