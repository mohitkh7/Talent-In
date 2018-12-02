from django.db import models

# Create your models here.
class Year(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(unique=True)

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=5, unique=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE, default=5)

    def __str__(self):
        return self.name

