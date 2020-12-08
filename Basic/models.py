from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class markDetails(models.Model):
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE,)
    semester = models.IntegerField()
    Department = models.CharField(max_length = 100)
    subject_name = models.CharField(max_length=100)
    marks = models.IntegerField()

class Departments(models.Model):
    name = models.CharField(max_length=100)