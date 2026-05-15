# rooms/migrations/0007_seed_all_data.py

from django.db import migrations

def create_data(apps, schema_editor):
    HotelRoomType = apps.get_model('rooms', 'HotelRoomType')
    RequiredElementSort = apps.get_model('rooms', 'RequiredElementSort')
    AdditionalElementSort = apps.get_model('rooms', 'AdditionalElementSort')
    RequiredHotelRoomElement = apps.get_model('rooms', 'RequiredHotelRoomElement')
    AdditionalHotelRoomElement = apps.get_model('rooms', 'AdditionalHotelRoomElement')
    RequiredIncompat = apps.get_model('rooms', 'IncompatibleHotelRoomElement_RequiredToRequired')
    AdditionalIncompat = apps.get_model('rooms', 'IncompatibleHotelRoomElement_AdditionalToAdditional')
    MixedIncompat = apps.get_model('rooms', 'IncompatibleHotelRoomElement_RequiredToAdditional')
    
    print("Создаю типы номеров...")
    room_types = {}
    for rt_name in ['Люкс', 'Стандарт', 'Эконом']:
        room_types[rt_name], _ = HotelRoomType.objects.get_or_create(name=rt_name)
    
    print("Создаю виды обязательных элементов...")
    required_sorts = {}
    for sort_name in ['Кровать', 'Раковина', 'Стол', 'Стул', 'Унитаз']:
        required_sorts[sort_name], _ = RequiredElementSort.objects.get_or_create(name=sort_name)
    
    print("Создаю виды дополнительных элементов...")
    additional_sorts = {}
    for sort_name in ['Кофеварка', 'Мультиварка', 'Отпариватель', 'Радиоприёмник', 
                      'Телевизор', 'Тостер', 'Увлажнитель воздуха', 'Холодильник']:
        additional_sorts[sort_name], _ = AdditionalElementSort.objects.get_or_create(name=sort_name)
    
    print("Создаю обязательные элементы...")
    required_elements_data = [
        # Люкс
        ("Кровать Премиум", "Кровать", "Люкс", 20000),
        ("Кровать С балдахином", "Кровать", "Люкс", 35000),
        ("Раковина Мраморная", "Раковина", "Люкс", 10000),
        ("Раковина Премиум", "Раковина", "Люкс", 5000),
        ("Стол Дуб", "Стол", "Люкс", 8000),
        ("Стол Красное дерево", "Стол", "Люкс", 12000),
        ("Стул Gigant Pro", "Стул", "Люкс", 2500),
        ("Стул Gigant Royal", "Стул", "Люкс", 5000),
        ("Унитаз Премиум", "Унитаз", "Люкс", 8000),
        ("Унитаз С подогревом", "Унитаз", "Люкс", 15000),
        # Стандарт
        ("Кровать Стандарт", "Кровать", "Стандарт", 8000),
        ("Раковина Стандарт", "Раковина", "Стандарт", 2500),
        ("Стол Орех", "Стол", "Стандарт", 4000),
        ("Стул Gigant", "Стул", "Стандарт", 1200),
        ("Унитаз Стандарт", "Унитаз", "Стандарт", 3500),
        # Эконом
        ("Кровать Эконом", "Кровать", "Эконом", 3000),
        ("Раковина Компакт", "Раковина", "Эконом", 1200),
        ("Стол Простой", "Стол", "Эконом", 1500),
        ("Стул Простой", "Стул", "Эконом", 500),
        ("Унитаз Компакт", "Унитаз", "Эконом", 2000),
    ]
    
    for name, sort_name, room_name, cost in required_elements_data:
        RequiredHotelRoomElement.objects.get_or_create(
            name=name,
            defaults={
                'element_sort': required_sorts[sort_name],
                'room_type': room_types[room_name],
                'cost': cost
            }
        )
    
    print("Создаю дополнительные элементы...")
    additional_elements_data = [
        # Люкс
        ("Кофеварка Jura", "Кофеварка", "Люкс", 25000),
        ("Кофеварка Saeco", "Кофеварка", "Люкс", 20000),
        ("Мультиварка Moulinex Premium", "Мультиварка", "Люкс", 10000),
        ("Мультиварка Vitek Premium", "Мультиварка", "Люкс", 8000),
        ("Отпариватель Philips Elite", "Отпариватель", "Люкс", 6000),
        ("Отпариватель Tefal Premium", "Отпариватель", "Люкс", 5000),
        ("Радиоприемник Bang & Olufsen", "Радиоприёмник", "Люкс", 15000),
        ("Радиоприемник Philips Premium", "Радиоприёмник", "Люкс", 5000),
        ("Телевизор LG OLED 55", "Телевизор", "Люкс", 50000),
        ("Телевизор Sony 65", "Телевизор", "Люкс", 80000),
        ("Тостер Bosch Plus", "Тостер", "Люкс", 5000),
        ("Тостер Dualit Classic", "Тостер", "Люкс", 8000),
        ("Увлажнитель воздуха Boneco", "Увлажнитель воздуха", "Люкс", 10000),
        ("Увлажнитель воздуха Winia", "Увлажнитель воздуха", "Люкс", 12000),
        ("Холодильник Liebherr", "Холодильник", "Люкс", 40000),
        ("Холодильник Sub-Zero Pro", "Холодильник", "Люкс", 40000),
        # Стандарт
        ("Кофеварка De'Longhi", "Кофеварка", "Стандарт", 5000),
        ("Мультиварка Scarlett", "Мультиварка", "Стандарт", 3500),
        ("Отпариватель Philips", "Отпариватель", "Стандарт", 1500),
        ("Радиоприемник Sony", "Радиоприёмник", "Стандарт", 2000),
        ("Телевизор LG 32", "Телевизор", "Стандарт", 15000),
        ("Тостер Tefal", "Тостер", "Стандарт", 2500),
        ("Увлажнитель воздуха Philips", "Увлажнитель воздуха", "Стандарт", 3000),
        ("Холодильник Indesit", "Холодильник", "Стандарт", 10000),
        # Эконом
        ("Мультиварка Redmond", "Мультиварка", "Эконом", 2000),
        ("Отпариватель Mystery", "Отпариватель", "Эконом", 4000),
        ("Телевизор Samsung 24", "Телевизор", "Эконом", 8000),
        ("Холодильник Бирюса", "Холодильник", "Эконом", 5000),
    ]
    
    for name, sort_name, room_name, cost in additional_elements_data:
        AdditionalHotelRoomElement.objects.get_or_create(
            name=name,
            defaults={
                'element_sort': additional_sorts[sort_name],
                'room_type': room_types[room_name],
                'cost': cost
            }
        )
    
    print("Создаю несовместимости...")
    
    required_incompat_data = [
        ("Кровать Премиум", "Кровать С балдахином"),
        ("Кровать Стандарт", "Кровать Эконом"),
        ("Стол Дуб", "Стол Орех"),
    ]
    
    for name1, name2 in required_incompat_data:
        el1 = RequiredHotelRoomElement.objects.get(name=name1)
        el2 = RequiredHotelRoomElement.objects.get(name=name2)
        RequiredIncompat.objects.get_or_create(element1=el1, element2=el2)
    
    additional_incompat_data = [
        ("Кофеварка De'Longhi", "Кофеварка Jura"),
        ("Радиоприемник Bang & Olufsen", "Радиоприемник Philips Premium"),
        ("Тостер Dualit Classic", "Тостер Tefal"),
    ]
    
    for name1, name2 in additional_incompat_data:
        el1 = AdditionalHotelRoomElement.objects.get(name=name1)
        el2 = AdditionalHotelRoomElement.objects.get(name=name2)
        AdditionalIncompat.objects.get_or_create(element1=el1, element2=el2)
    
    mixed_incompat_data = [
        ("Унитаз С подогревом", "Холодильник Sub-Zero Pro"),
        ("Кровать Стандарт", "Радиоприемник Sony"),
        ("Унитаз С подогревом", "Отпариватель Mystery"),
        ("Раковина Мраморная", "Отпариватель Mystery"),
    ]
    
    for name1, name2 in mixed_incompat_data:
        el1 = RequiredHotelRoomElement.objects.get(name=name1)
        el2 = AdditionalHotelRoomElement.objects.get(name=name2)
        MixedIncompat.objects.get_or_create(element1=el1, element2=el2)
    
    print("Все данные успешно созданы!")


def delete_data(apps, schema_editor):
    """Удаление всех данных (функция отката)"""
    
    RequiredIncompat = apps.get_model('rooms', 'IncompatibleHotelRoomElement_RequiredToRequired')
    AdditionalIncompat = apps.get_model('rooms', 'IncompatibleHotelRoomElement_AdditionalToAdditional')
    MixedIncompat = apps.get_model('rooms', 'IncompatibleHotelRoomElement_RequiredToAdditional')
    RequiredHotelRoomElement = apps.get_model('rooms', 'RequiredHotelRoomElement')
    AdditionalHotelRoomElement = apps.get_model('rooms', 'AdditionalHotelRoomElement')
    RequiredElementSort = apps.get_model('rooms', 'RequiredElementSort')
    AdditionalElementSort = apps.get_model('rooms', 'AdditionalElementSort')
    HotelRoomType = apps.get_model('rooms', 'HotelRoomType')
    
    # Удаляем в обратном порядке (сначала связанные данные)
    RequiredIncompat.objects.all().delete()
    AdditionalIncompat.objects.all().delete()
    MixedIncompat.objects.all().delete()
    RequiredHotelRoomElement.objects.all().delete()
    AdditionalHotelRoomElement.objects.all().delete()
    RequiredElementSort.objects.all().delete()
    AdditionalElementSort.objects.all().delete()
    HotelRoomType.objects.all().delete()
    
    print("Все данные удалены!")


class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0006_additionalelementsort_additionalhotelroomelement_and_more'),
    ]

    operations = [
        migrations.RunPython(create_data, delete_data),
    ]