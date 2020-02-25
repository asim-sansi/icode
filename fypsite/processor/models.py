from django.db import models


# Create your models here.

class Template(models.Model):
    name = models.CharField(max_length=100)
    filename = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def filename(self):
        return self.filename
