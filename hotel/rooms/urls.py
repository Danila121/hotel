from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path("", views.room_type, name="room_type"),
    path("index/", views.index, name="index"),
    path("generate/", views.generate_variants, name="generate_variants"),
]