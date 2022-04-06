from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    idSubject = models.CharField(max_length=5, primary_key=True)

class Assignment(models.Model):
    idSubject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment = models.CharField(max_length=5)
    score = models.CharField(max_length=6)
    result = models.CharField(max_length=256)
    pathMainFile = models.CharField(max_length=256)
    pathInput = models.CharField(max_length=256)
    pathOutput = models.CharField(max_length=256)
    language = models.CharField(max_length=32)
    format = models.BooleanField(default=False)
    error = models.BooleanField(default=True)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    idSubject = models.ManyToManyField(Subject, blank=True)

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idSubject = models.CharField(max_length=5)
    assignment = models.CharField(max_length=5)
    score = models.CharField(max_length=6)
    timeIn = models.CharField(max_length=32)
    check = models.BooleanField(default=False)
    error = models.CharField(max_length=256)