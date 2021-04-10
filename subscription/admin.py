from django.contrib import admin
from subscription import models as sub_models


@admin.register(sub_models.Student)
class AdminModelStudent(admin.ModelAdmin):
    list_display = [field.name for field in sub_models.Student._meta.get_fields()]
