from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.utils.html import strip_tags

class Test(models.Model):
    content = RichTextField(default="Hello World")

class wordToCriteria(models.Model):
    content = RichTextField(default="Hello World")

class uniqueCriteria(models.Model):
    content = RichTextField(default="Hello World")

class regForCriteria(models.Model):
    content = RichTextField(default="Hello World")

