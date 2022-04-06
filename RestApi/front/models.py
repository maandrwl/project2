
from pydoc import describe
from django.db import models

# Create your models here.

class Item(models.Model):
    CourseName = models.CharField(max_length=100, null=True,unique=True)
    code = models.CharField(max_length=5, null=True,unique=True)
    semester = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    

    def __str__(self):
        return self.code


class Assign(models.Model):
    Assignment = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True,blank=True)
    language = models.CharField(max_length=32,null=True)
    #pdf = models.FileField(upload_to='assigns/pdfs')
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_updated = models.DateTimeField(auto_now=True)
    score = models.CharField(max_length=6)

    def __str__(self):
        return self.Assignment