from django.shortcuts import render, get_object_or_404
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
import itertools


def room_type(request):
    """Страница выбора типа номера"""
    room_types = HotelRoomType.objects.all()
    return render(request, 'room_type.html', {'room_types': room_types})


def index(request):
    """Страница с элементами для выбранного типа номера"""
    room_type_name = request.GET.get('room_type')
    
    if not room_type_name:
        room_types = HotelRoomType.objects.all()
        return render(request, 'room_type.html', {'room_types': room_types})
    
    room_type = get_object_or_404(HotelRoomType, name=room_type_name)
    
    # Получаем обязательные элементы
    required_elements = RequiredHotelRoomElement.objects.filter(
        room_type=room_type
    ).select_related("element_sort")
    
    # Получаем дополнительные элементы
    additional_elements = AdditionalHotelRoomElement.objects.filter(
        room_type=room_type
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
            "id": el.name,
            "cost": el.cost,
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
            "id": el.name,
            "cost": el.cost,
        })

    # Сбор несовместимостей
    incompat_list = []

    required_incompat = IncompatibleHotelRoomElement_RequiredToRequired.objects.filter(
        element1__room_type=room_type
    ).select_related("element1", "element2")

    for inc in required_incompat:
        incompat_list.append([inc.element1.name, inc.element2.name])

    additional_incompat = IncompatibleHotelRoomElement_AdditionalToAdditional.objects.filter(
        element1__room_type=room_type
    ).select_related("element1", "element2")

    for inc in additional_incompat:
        incompat_list.append([inc.element1.name, inc.element2.name])

    cross_incompat = IncompatibleHotelRoomElement_RequiredToAdditional.objects.filter(
        element1__room_type=room_type
    ).select_related("element1", "element2")

    for inc in cross_incompat:
        incompat_list.append([inc.element1.name, inc.element2.name])

    types_data = [{
        "room_type": room_type.name,
        "sorts": list(sorts_dict.values()),
        "incompatibilities": incompat_list,
    }]

    context = {
        "room_type": room_type,
        "room_types": HotelRoomType.objects.all(),
        "types_data_json": json.dumps(types_data, ensure_ascii=False),
    }
    return render(request, "index.html", context)


def generate_variants(request):
    """API для генерации вариантов комплектации - GET запрос"""
    if request.method == 'GET':
        room_type_name = request.GET.get('room_type')
        selected_str = request.GET.get('selected', '[]')
        budget_str = request.GET.get('budget', '')
        
        try:
            selected = json.loads(selected_str)
        except json.JSONDecodeError:
            selected = []
        
        budget = float(budget_str) if budget_str else None
        
        if not room_type_name:
            return JsonResponse({'error': 'room_type required'}, status=400)
        
        try:
            room_type = HotelRoomType.objects.get(name=room_type_name)
        except HotelRoomType.DoesNotExist:
            return JsonResponse({'error': 'Room type not found'}, status=404)
        
        # === 1. ОБЯЗАТЕЛЬНЫЕ ЭЛЕМЕНТЫ ===
        # Получаем все категории обязательных элементов
        required_sorts = RequiredHotelRoomElement.objects.filter(
            room_type=room_type
        ).select_related('element_sort').values_list('element_sort__name', flat=True).distinct()
        
        # Фиксируем выбранные обязательные элементы
        selected_required_names = [s['element'] for s in selected if s.get('is_required', False)]
        
        # Собираем доступные варианты для каждой категории
        categories_options = {}
        for sort_name in required_sorts:
            elements = RequiredHotelRoomElement.objects.filter(
                room_type=room_type,
                element_sort__name=sort_name
            )
            
            # Проверяем, выбран ли элемент в этой категории
            selected_in_sort = [el for el in elements if el.name in selected_required_names]
            
            if selected_in_sort:
                # Если выбран - только этот вариант
                categories_options[sort_name] = [selected_in_sort[0]]
            else:
                # Если не выбран - все варианты
                categories_options[sort_name] = list(elements)
        
        # Генерируем комбинации обязательных элементов
        all_combinations = list(itertools.product(*categories_options.values()))
        
        # === 2. ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ ===
        # Получаем ВСЕ выбранные дополнительные элементы
        selected_additional = []
        for sel in selected:
            if not sel.get('is_required', True):  # Это дополнительный элемент
                try:
                    additional = AdditionalHotelRoomElement.objects.get(
                        name=sel['element'],
                        room_type=room_type
                    )
                    selected_additional.append(additional)
                except AdditionalHotelRoomElement.DoesNotExist:
                    pass
        
        # Фильтруем комбинации по несовместимостям и бюджету
        valid_combinations = []
        
        for combination in all_combinations:
            # Проверка несовместимостей между обязательными элементами
            if not check_required_incompatibilities(combination, room_type):
                continue
            
            # Объединяем обязательные элементы с выбранными дополнительными
            all_elements = list(combination) + selected_additional
            
            # Проверка несовместимостей между обязательными и дополнительными
            if not check_mixed_incompatibilities(combination, selected_additional, room_type):
                continue
            
            total_cost = sum(el.cost for el in combination) + sum(el.cost for el in selected_additional)
            
            if budget and total_cost > budget:
                continue
            
            valid_combinations.append({
                'elements': [{'name': el.name, 'cost': el.cost} for el in all_elements],
                'total_cost': total_cost
            })
        
        # Сортируем по стоимости
        valid_combinations.sort(key=lambda x: x['total_cost'])
        
        # Ограничиваем количество результатов (первые 50)
        valid_combinations = valid_combinations[:50]
        
        return JsonResponse({'variants': valid_combinations})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def check_required_incompatibilities(combination, room_type):
    """Проверка несовместимостей между обязательными элементами"""
    element_names = [el.name for el in combination]
    
    incompatibilities = IncompatibleHotelRoomElement_RequiredToRequired.objects.filter(
        element1__room_type=room_type
    ).select_related('element1', 'element2')
    
    for inc in incompatibilities:
        if inc.element1.name in element_names and inc.element2.name in element_names:
            return False
    
    return True


def check_mixed_incompatibilities(required_elements, additional_elements, room_type):
    """Проверка несовместимостей между обязательными и дополнительными элементами"""
    required_names = [el.name for el in required_elements]
    additional_names = [el.name for el in additional_elements]
    
    incompatibilities = IncompatibleHotelRoomElement_RequiredToAdditional.objects.filter(
        element1__room_type=room_type
    ).select_related('element1', 'element2')
    
    for inc in incompatibilities:
        # Проверяем все пары
        if inc.element1.name in required_names and inc.element2.name in additional_names:
            return False
        if inc.element1.name in additional_names and inc.element2.name in required_names:
            return False
    
    return True