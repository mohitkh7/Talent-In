from django.db import models

# Create your models here.
class Year(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(unique=True)

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=5, unique=True)