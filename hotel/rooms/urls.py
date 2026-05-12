from . import views
from django.urls import path
app_name = 'rooms'


urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
]
