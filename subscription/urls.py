from django.urls import path
from subscription import views as sub_views

urlpatterns = [
    path('register/', sub_views.register_student, name='register'),
]
