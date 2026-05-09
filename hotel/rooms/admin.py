from django.contrib import admin
from .models import RoomElement, RoomType, Room, ElementType, IncompatibleRoomElement, RoomElementAssignment
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RoomElement)
admin.site.register(ElementType)
admin.site.register(IncompatibleRoomElement)
admin.site.register(RoomElementAssignment)