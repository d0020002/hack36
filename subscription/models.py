from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    student_name = models.CharField(null=False, blank=False, max_length=200)
    student_class = models.IntegerField(null=False, blank=False)
    student_phone = models.CharField(max_length=10, null=False, blank=False)


class Topic(models.Model):
    heading = models.CharField(max_length=100, null=False)
    body = models.CharField(max_length=300, null=False)


class Subject(models.Model):
    topics = models.ManyToManyField(Topic)
