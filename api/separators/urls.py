from django.urls import path
from . import views

urlpatterns = [
    path("separators/", views.index, name="index"),
]