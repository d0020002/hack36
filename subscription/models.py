from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    student_name = models.CharField(null=False, blank=False, max_length=200)
    student_class = models.CharField(max_length=10, null=False, blank=False)
    student_phone = models.CharField(max_length=10, null=False, blank=False)
    student_subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return "Name :" + self.student_name + " - Class: " + self.student_class


class Subject(models.Model):
    subject_name = models.CharField(max_length=100, null=False, blank=False)
    subject_class = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.subject_name + " Class " + self.subject_class


class Chapter(models.Model):
    index = models.PositiveSmallIntegerField()
    heading = models.CharField(max_length=100, null=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.subject) + " - " + str(self.index) + " - " + self.heading


class Topic(models.Model):
    index = models.PositiveSmallIntegerField(default=1)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    heading = models.CharField(max_length=100, null=False)
    body = models.CharField(max_length=300, null=False)


class Progress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    last_topic_index = models.PositiveSmallIntegerField(default=0)
    last_topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    last_chapter_index = models.PositiveSmallIntegerField(default=0)
    last_chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE)
