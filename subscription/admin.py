from django.contrib import admin
from subscription import models as sub_models


@admin.register(sub_models.Student)
class AdminModelStudent(admin.ModelAdmin):
    list_display = ["student_name", "student_class", "student_phone"]


@admin.register(sub_models.Subject)
class AdminModelSubject(admin.ModelAdmin):
    list_display = ["subject_name", "subject_class"]


@admin.register(sub_models.Chapter)
class AdminModelChapter(admin.ModelAdmin):
    list_display = [field.name for field in sub_models.Chapter._meta.fields]


@admin.register(sub_models.Topic)
class AdminModelTopic(admin.ModelAdmin):
    list_display = ["chapter", "heading", "body"]


@admin.register(sub_models.Progress)
class AdminModelProgress(admin.ModelAdmin):
    list_display = ["student", "subject", "last_topic", "last_chapter"]
