
from enum import unique
from pydoc import describe
from pyexpat import model
from django.template.defaultfilters import slugify
from django.db import models
from django.urls import reverse

# Create your models here.



class Item(models.Model):
    CourseName = models.CharField(max_length=100, null=True,)
    code = models.CharField(max_length=5, null=True)
    semester = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    slug = models.SlugField(null=True, blank=True)
    class Meta:
        unique_together = ["CourseName","code","semester","year"]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Assign(models.Model):
    Assignment = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True,blank=True)
    language = models.CharField(max_length=32,null=True)
    #pdf = models.FileField(upload_to='assigns/pdfs')
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_updated = models.DateTimeField(auto_now=True)
    score = models.CharField(max_length=6)
    subject = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.Assignment

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('assign_list', kwargs={'slug':self.subject.slug})