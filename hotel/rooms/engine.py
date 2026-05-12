from itertools import product
from .models import HotelRoomType, HotelRoomElement, ElementSort, IncompatibleRoomElement


def get_allowed_elements(room_type_name, selected):
    """
    Принимает:
        room_type_name: str - название типа номера (например "Стандарт")
        selected: list of dict - [{"element": "Имя", "quantity": 1}, ...]
    Возвращает:
        list of list of dict - допустимые варианты, каждый вариант:
        [
            {"name": "Кровать МОРИ ЛЮКС", "quantity": 1},
            {"name": "Стол Дуб", "quantity": 1},
            ...
        ]
    """
    try:
        room_type = HotelRoomType.objects.get(name=room_type_name)
    except HotelRoomType.DoesNotExist:
        return []

    # Все сорта (их обязательность)
    sorts = ElementSort.objects.all()
    sort_required = {s.name: s.is_required for s in sorts}

    # Все элементы выбранного типа с подгрузкой сорта
    elements = HotelRoomElement.objects.filter(
        room_type=room_type
    ).select_related("element_sort")

    # Группируем элементы по названию сорта
    sort_elements = {}
    for el in elements:
        sort_name = el.element_sort.name
        sort_elements.setdefault(sort_name, []).append(el)

    # Множество имён элементов, выбранных пользователем
    selected_names = {item["element"] for item in selected if item.get("quantity", 0) > 0}

    # Собираем варианты для обязательных сортов и фиксированные необязательные элементы
    mandatory_variants = []   # список списков элементов (варианты для каждого обязательного сорта)
    optional_fixed = []      # список выбранных необязательных элементов

    for sort_name, els in sort_elements.items():
        is_req = sort_required.get(sort_name, False)

        # Выбранные пользователем элементы данного сорта
        chosen = [el for el in els if el.name in selected_names]

        if is_req:
            if chosen:
                # Пользователь выбрал один элемент в обязательном сорте -> фиксируем его
                mandatory_variants.append([chosen[0]])
            else:
                # Не выбрал -> все элементы этого сорта становятся вариантами
                if els:
                    mandatory_variants.append(list(els))
                # Если элементов нет (ошибка данных) – игнорируем сорт
        else:
            if chosen:
                # Необязательный сорт: если выбран – добавляем в фиксированный набор
                optional_fixed.extend(chosen)
            # иначе ничего не добавляем

    # Декартово произведение обязательных вариантов
    if not mandatory_variants:
        base_combinations = [tuple()]
    else:
        base_combinations = product(*mandatory_variants)

    # Загружаем несовместимости для этого типа номера
    incompat = IncompatibleRoomElement.objects.filter(element__room_type=room_type)
    forbidden_pairs = set()
    for inc in incompat:
        n1 = inc.element.name
        n2 = inc.incompatible_element.name
        forbidden_pairs.add(frozenset([n1, n2]))

    valid_variants = []
    for combo in base_combinations:
        # combo – кортеж элементов обязательных сортов
        all_items = list(combo) + optional_fixed
        if _is_compatible(all_items, forbidden_pairs):
            variant = [{"name": el.name, "quantity": 1} for el in all_items]
            valid_variants.append(variant)

    return valid_variants


def _is_compatible(items, forbidden_pairs):
    """Проверяет, что среди элементов нет ни одной несовместимой пары."""
    names = [el.name for el in items]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if frozenset([names[i], names[j]]) in forbidden_pairs:
                return False
    return True