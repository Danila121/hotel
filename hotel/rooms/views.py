from django.shortcuts import render
from django.http import JsonResponse
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
import json


def index(request):
    room_types = HotelRoomType.objects.all()
    types_data = []
    
    for rt in room_types:
        # ИСПРАВЛЕНО: получаем обязательные элементы
        required_elements = RequiredHotelRoomElement.objects.filter(
            room_type=rt
        ).select_related("element_sort")
        
        # ИСПРАВЛЕНО: получаем дополнительные элементы (не сортировки!)
        additional_elements = AdditionalHotelRoomElement.objects.filter(
            room_type=rt
        ).select_related("element_sort")

        sorts_dict = {}

        # Обработка обязательных элементов
        for el in required_elements:
            sort_name = el.element_sort.name
            if sort_name not in sorts_dict:
                sorts_dict[sort_name] = {
                    "name": sort_name,
                    "is_required": True,
                    "elements": [],
                }
            sorts_dict[sort_name]["elements"].append({
                "name": el.name,
                "id": el.name,  # primary_key - это name
            })

        # Обработка дополнительных элементов
        for el in additional_elements:
            sort_name = el.element_sort.name
            if sort_name not in sorts_dict:
                sorts_dict[sort_name] = {
                    "name": sort_name,
                    "is_required": False,
                    "elements": [],
                }
            sorts_dict[sort_name]["elements"].append({
                "name": el.name,
                "id": el.name,  # primary_key - это name
            })

        incompat_list = []

        # Несовместимости обязательных с обязательными
        required_incompat = IncompatibleHotelRoomElement_RequiredToRequired.objects.filter(
            element1__room_type=rt
        ).select_related("element1", "element2")

        for inc in required_incompat:
            incompat_list.append([inc.element1.name, inc.element2.name])

        # Несовместимости дополнительных с дополнительными
        # ИСПРАВЛЕНО: используем additional_incompat, а не required_incompat
        additional_incompat = IncompatibleHotelRoomElement_AdditionalToAdditional.objects.filter(
            element1__room_type=rt
        ).select_related("element1", "element2")

        for inc in additional_incompat:  # ИСПРАВЛЕНО
            incompat_list.append([inc.element1.name, inc.element2.name])

        # Несовместимости обязательных с дополнительными
        # ИСПРАВЛЕНО: используем cross_incompat и правильную переменную в цикле
        cross_incompat = IncompatibleHotelRoomElement_RequiredToAdditional.objects.filter(
            element1__room_type=rt
        ).select_related("element1", "element2")

        for inc in cross_incompat:  # ИСПРАВЛЕНО
            incompat_list.append([inc.element1.name, inc.element2.name])

        types_data.append({
            "room_type": rt.name,
            "sorts": list(sorts_dict.values()),
            "incompatibilities": incompat_list,
        })

    context = {
        "room_types": room_types,
        "types_data_json": json.dumps(types_data, ensure_ascii=False),
    }
    return render(request, "index.html", context)


def generate_variants(request):
    """API для генерации вариантов элементов"""
    if request.method == 'POST':
        import json as json_lib
        data = json_lib.loads(request.body)
        selected_elements = data.get('selected_elements', [])
        room_type_name = data.get('room_type')
        
        # Здесь будет логика из engine.get_allowed_elements
        # Пока возвращаем пустой список
        return JsonResponse({'allowed_elements': []})