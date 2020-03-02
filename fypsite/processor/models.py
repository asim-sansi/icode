from django.db import models


# Create your models here.

class Template(models.Model):
    name = models.CharField(max_length=100)
    filename = models.CharField(max_length=150)
