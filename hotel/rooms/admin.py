from django.contrib import admin
from .models import (
    RequiredHotelRoomElement,
    AdditionalHotelRoomElement,
    HotelRoomType,
    RequiredElementSort,
    AdditionalElementSort,
    IncompatibleHotelRoomElement_RequiredToRequired,
    IncompatibleHotelRoomElement_AdditionalToAdditional,
    IncompatibleHotelRoomElement_RequiredToAdditional,
)

admin.site.register(RequiredHotelRoomElement)
admin.site.register(AdditionalHotelRoomElement)
admin.site.register(HotelRoomType)
admin.site.register(RequiredElementSort)
admin.site.register(AdditionalElementSort)
admin.site.register(IncompatibleHotelRoomElement_RequiredToRequired)
admin.site.register(IncompatibleHotelRoomElement_AdditionalToAdditional)
admin.site.register(IncompatibleHotelRoomElement_RequiredToAdditional)
