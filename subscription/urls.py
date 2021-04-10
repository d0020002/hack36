from django.urls import path
from subscription import views as sub_views

urlpatterns = [
    path('register/', sub_views.register_student, name='register'),
    path('search/', sub_views.search, name='search'),
]
