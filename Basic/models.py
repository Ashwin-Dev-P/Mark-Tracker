from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
class Departments(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
class semester(models.Model):
    id = models.BigAutoField(primary_key=True)
    semester = models.PositiveSmallIntegerField( validators=[MaxValueValidator(12)])

class markDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE,)
    semester = models.PositiveSmallIntegerField( validators=[MaxValueValidator(12)])
    subject_name = models.CharField(max_length=100)
    marks = models.PositiveSmallIntegerField(validators=[MaxValueValidator(101)])



class additionalInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE,)
    Department = models.ForeignKey(Departments,default=None,on_delete=models.CASCADE)
    current_semester = models.ForeignKey(semester,default=None,validators=[MaxValueValidator(101)],on_delete=models.CASCADE)
    privacy = models.PositiveSmallIntegerField(default=0,validators = [MaxValueValidator(1)]);

class subjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)