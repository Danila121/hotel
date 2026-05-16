# engine.py
from itertools import product
from .models import RequiredHotelRoomElement, AdditionalHotelRoomElement


def get_allowed_elements(room_type, selected_required, budget=None):
    """
    Генерация возможных комплектаций
    
    Args:
        room_type: объект типа номера
        selected_required: список выбранных обязательных элементов [{"element": "name", "quantity": 1}]
        budget: бюджет пользователя (руб.)
    
    Returns:
        list: список возможных комплектаций
    """
    
    # 1. Получаем все виды обязательных элементов для данного типа номера
    required_sorts = RequiredHotelRoomElement.objects.filter(
        room_type=room_type
    ).select_related('element_sort').values_list('element_sort__name', flat=True).distinct()
    
    # 2. Собираем словарь: вид элемента -> список доступных элементов
    categories = {}
    for sort_name in required_sorts:
        elements = RequiredHotelRoomElement.objects.filter(
            room_type=room_type,
            element_sort__name=sort_name
        )
        categories[sort_name] = list(elements)
    
    # 3. Фиксируем выбранные пользователем элементы
    fixed_elements = {}
    for selected in selected_required:
        element_name = selected['element']
        try:
            element = RequiredHotelRoomElement.objects.get(name=element_name)
            sort_name = element.element_sort.name
            fixed_elements[sort_name] = element
        except RequiredHotelRoomElement.DoesNotExist:
            pass
    
    # 4. Формируем списки для перебора (учитывая фиксированные элементы)
    variants_categories = []
    category_names = []
    
    for sort_name in categories:
        if sort_name in fixed_elements:
            # Если элемент выбран пользователем - только он
            variants_categories.append([fixed_elements[sort_name]])
        else:
            # Если не выбран - все возможные элементы
            variants_categories.append(categories[sort_name])
        category_names.append(sort_name)
    
    # 5. Генерируем все комбинации (декартово произведение)
    all_combinations = list(product(*variants_categories))
    
    # 6. Проверяем несовместимости и бюджет
    valid_combinations = []
    
    for combination in all_combinations:
        # Проверка несовместимостей
        if not check_incompatibilities(combination, room_type):
            continue
        
        # Расчет стоимости
        total_cost = sum(el.cost for el in combination)
        
        # Проверка бюджета
        if budget and total_cost > budget:
            continue
        
        # Сохраняем валидную комбинацию
        valid_combinations.append({
            'elements': combination,
            'total_cost': total_cost
        })
    
    # 7. Сортируем по стоимости
    valid_combinations.sort(key=lambda x: x['total_cost'])
    
    return valid_combinations


def check_incompatibilities(combination, room_type):
    """
    Проверка наличия несовместимых элементов в комбинации
    """
    from .models import (
        IncompatibleHotelRoomElement_RequiredToRequired,
        IncompatibleHotelRoomElement_AdditionalToAdditional,
        IncompatibleHotelRoomElement_RequiredToAdditional
    )
    
    element_names = [el.name for el in combination]
    
    # Проверка несовместимостей между обязательными элементами
    required_incompat = IncompatibleHotelRoomElement_RequiredToRequired.objects.filter(
        element1__room_type=room_type
    ).select_related('element1', 'element2')
    
    for inc in required_incompat:
        if inc.element1.name in element_names and inc.element2.name in element_names:
            return False
    
    return True


def add_additional_elements(combination, selected_additional, budget, total_cost):
    """
    Добавление дополнительных элементов к комплектации
    """
    if not selected_additional:
        return [combination]
    
    # Получаем выбранные дополнительные элементы
    additional_elements = []
    for selected in selected_additional:
        element_name = selected['element']
        try:
            element = AdditionalHotelRoomElement.objects.get(name=element_name)
            additional_elements.append(element)
        except AdditionalHotelRoomElement.DoesNotExist:
            pass
    
    # Добавляем к стоимости
    additional_cost = sum(el.cost for el in additional_elements)
    total_cost += additional_cost
    
    # Проверяем бюджет
    if budget and total_cost > budget:
        return None
    
    # Возвращаем комплектацию с дополнительными элементами
    return {
        'elements': combination['elements'] + additional_elements,
        'total_cost': total_cost
    }