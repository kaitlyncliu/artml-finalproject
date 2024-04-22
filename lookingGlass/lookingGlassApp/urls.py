from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("animate", views.animate, name="animate"),
    path("process_audio", views.process_audio, name="process_audio")
]