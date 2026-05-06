from django.db import migrations

def seed_room_elements(apps, schema_editor):
    RoomElement = apps.get_model('rooms', 'RoomElement')
    ElementType = apps.get_model('rooms', 'ElementType')
    RoomType = apps.get_model('rooms', 'RoomType')

    # Типы элементов
    bed = ElementType.objects.get(name='Кровать')
    table = ElementType.objects.get(name='Стол')
    chair = ElementType.objects.get(name='Стул')
    toilet = ElementType.objects.get(name='Унитаз')
    sink = ElementType.objects.get(name='Раковина')
    fridge = ElementType.objects.get(name='Холодильник')
    tv = ElementType.objects.get(name='Телевизор')
    coffee = ElementType.objects.get(name='Кофеварка')
    toaster = ElementType.objects.get(name='Тостер')
    radio = ElementType.objects.get(name='Радиоприемник')

    # Типы комнат
    economy = RoomType.objects.get(name='Эконом')
    standard = RoomType.objects.get(name='Стандарт')
    luxury = RoomType.objects.get(name='Люкс')

    # ===== Эконом =====
    RoomElement.objects.get_or_create(name='Кровать односпальная 90×200', element_type=bed, room_type=economy)
    RoomElement.objects.get_or_create(name='Кровать полуторная 120×200', element_type=bed, room_type=economy)
    RoomElement.objects.get_or_create(name='Стол складной пластиковый', element_type=table, room_type=economy)
    RoomElement.objects.get_or_create(name='Стол обеденный малый', element_type=table, room_type=economy)
    RoomElement.objects.get_or_create(name='Стул пластиковый', element_type=chair, room_type=economy)
    RoomElement.objects.get_or_create(name='Стул деревянный складной', element_type=chair, room_type=economy)
    RoomElement.objects.get_or_create(name='Унитаз компакт эконом', element_type=toilet, room_type=economy)
    RoomElement.objects.get_or_create(name='Унитаз напольный эконом', element_type=toilet, room_type=economy)
    RoomElement.objects.get_or_create(name='Раковина керамическая малая', element_type=sink, room_type=economy)
    RoomElement.objects.get_or_create(name='Раковина угловая компакт', element_type=sink, room_type=economy)

    # ===== Стандарт =====
    RoomElement.objects.get_or_create(name='Кровать двуспальная 160×200', element_type=bed, room_type=standard)
    RoomElement.objects.get_or_create(name='Кровать двуспальная 140×200', element_type=bed, room_type=standard)
    RoomElement.objects.get_or_create(name='Стол письменный', element_type=table, room_type=standard)
    RoomElement.objects.get_or_create(name='Стол журнальный', element_type=table, room_type=standard)
    RoomElement.objects.get_or_create(name='Стол туалетный с зеркалом', element_type=table, room_type=standard)
    RoomElement.objects.get_or_create(name='Стул офисный', element_type=chair, room_type=standard)
    RoomElement.objects.get_or_create(name='Стул эргономичный', element_type=chair, room_type=standard)
    RoomElement.objects.get_or_create(name='Унитаз подвесной', element_type=toilet, room_type=standard)
    RoomElement.objects.get_or_create(name='Унитаз напольный стандарт', element_type=toilet, room_type=standard)
    RoomElement.objects.get_or_create(name='Раковина прямоугольная', element_type=sink, room_type=standard)
    RoomElement.objects.get_or_create(name='Раковина овальная керамика', element_type=sink, room_type=standard)
    RoomElement.objects.get_or_create(name='Телевизор LED 32"', element_type=tv, room_type=standard)
    RoomElement.objects.get_or_create(name='Телевизор LCD 24"', element_type=tv, room_type=standard)
    RoomElement.objects.get_or_create(name='Холодильник мини', element_type=fridge, room_type=standard)
    RoomElement.objects.get_or_create(name='Холодильник без морозилки', element_type=fridge, room_type=standard)
    RoomElement.objects.get_or_create(name='Радиоприемник портативный', element_type=radio, room_type=standard)

    # ===== Люкс =====
    RoomElement.objects.get_or_create(name='Кровать King-size 200×200', element_type=bed, room_type=luxury)
    RoomElement.objects.get_or_create(name='Кровать Queen-size 180×200', element_type=bed, room_type=luxury)
    RoomElement.objects.get_or_create(name='Кровать детская 90×180', element_type=bed, room_type=luxury)
    RoomElement.objects.get_or_create(name='Стол обеденный раздвижной', element_type=table, room_type=luxury)
    RoomElement.objects.get_or_create(name='Стол рабочий Executive', element_type=table, room_type=luxury)
    RoomElement.objects.get_or_create(name='Стол сервировочный', element_type=table, room_type=luxury)
    RoomElement.objects.get_or_create(name='Стул кожаный Chesterfield', element_type=chair, room_type=luxury)
    RoomElement.objects.get_or_create(name='Стул барный', element_type=chair, room_type=luxury)
    RoomElement.objects.get_or_create(name='Стул дизайнерский Eames', element_type=chair, room_type=luxury)
    RoomElement.objects.get_or_create(name='Унитаз с биде-функцией', element_type=toilet, room_type=luxury)
    RoomElement.objects.get_or_create(name='Унитаз умный с подогревом', element_type=toilet, room_type=luxury)
    RoomElement.objects.get_or_create(name='Раковина двойная мраморная', element_type=sink, room_type=luxury)
    RoomElement.objects.get_or_create(name='Раковина дизайнерская стеклянная', element_type=sink, room_type=luxury)
    RoomElement.objects.get_or_create(name='Телевизор OLED 55"', element_type=tv, room_type=luxury)
    RoomElement.objects.get_or_create(name='Телевизор QLED 65"', element_type=tv, room_type=luxury)
    RoomElement.objects.get_or_create(name='Холодильник мини-бар', element_type=fridge, room_type=luxury)
    RoomElement.objects.get_or_create(name='Холодильник встроенный', element_type=fridge, room_type=luxury)
    RoomElement.objects.get_or_create(name='Кофеварка капсульная Nespresso', element_type=coffee, room_type=luxury)
    RoomElement.objects.get_or_create(name='Кофеварка рожковая DeLonghi', element_type=coffee, room_type=luxury)
    RoomElement.objects.get_or_create(name='Тостер премиум Smeg', element_type=toaster, room_type=luxury)
    RoomElement.objects.get_or_create(name='Тостер с подогревом булочек', element_type=toaster, room_type=luxury)
    RoomElement.objects.get_or_create(name='Радиоприемник Hi-Fi Yamaha', element_type=radio, room_type=luxury)
    RoomElement.objects.get_or_create(name='Радиоприемник с Bluetooth Bose', element_type=radio, room_type=luxury)

class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0004_seed_rooms'),
    ]
    operations = [
        migrations.RunPython(seed_room_elements),
    ]