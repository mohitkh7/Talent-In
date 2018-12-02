from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Year(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.short_name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=5)

    class Meta:
        ordering = ['category']
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    year = models.ForeignKey('Year', on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField('Skill')

    contact_number = models.PositiveIntegerField(null=True)
    facebook_url = models.URLField(null=True, blank=True, default="http://www.facebook.com")
    linkedin_url = models.URLField(null=True, blank=True, default="http://www.linkedin.com")
    github_url = models.URLField(null=True, blank=True, default="http://www.github.com")

    def __str__(self):
        return self.name
