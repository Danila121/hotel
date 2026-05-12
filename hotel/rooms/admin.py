from django.contrib import admin
from .models import HotelRoomElement, HotelRoomType, ElementSort, IncompatibleRoomElement
admin.site.register(HotelRoomType)
admin.site.register(HotelRoomElement)
admin.site.register(ElementSort)
admin.site.register(IncompatibleRoomElement)