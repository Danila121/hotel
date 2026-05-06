from . import views
from django.urls import path
app_name = 'rooms'


urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'rooms/<int:pk>/',
        views.room_detail,
        name='room_detail'
    ),
    path(
        'rooms',
        views.rooms,
        name='rooms'
    ),
    path(
        'elements',
        views.elements,
        name='elements'
    ),
    path(
        'incompatible-elements',
        views.incompatible_elements,
        name='incompatible_elements'
    ),
    path(
        'select/',
        views.select_room,
        name='select_room'
    ),
]
