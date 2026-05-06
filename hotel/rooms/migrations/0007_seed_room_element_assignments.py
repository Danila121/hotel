from django.db import migrations

def seed_assignments(apps, schema_editor):
    Room = apps.get_model('rooms', 'Room')
    RoomElement = apps.get_model('rooms', 'RoomElement')
    RoomElementAssignment = apps.get_model('rooms', 'RoomElementAssignment')

    # Получаем комнаты
    room1 = Room.objects.get(id=1)
    room2 = Room.objects.get(id=2)
    room3 = Room.objects.get(id=3)
    room4 = Room.objects.get(id=4)
    room5 = Room.objects.get(id=5)
    room6 = Room.objects.get(id=6)

    # ---------- ЭКОНОМ (комнаты 4 и 5) ----------
    # Обязательные элементы: кровать, стол, стул, унитаз, раковина.
    # остальные позиции – все доступные совместимые элементы.

    # Комната 4
    elems_room4 = [
        'Кровать односпальная 90×200',
        'Стул пластиковый',
        'Стол складной пластиковый',
        'Стол обеденный малый',
        'Унитаз компакт эконом',
        'Раковина керамическая малая',
    ]
    for name in elems_room4:
        elem = RoomElement.objects.get(name=name)
        RoomElementAssignment.objects.get_or_create(room=room4, element=elem)

    # Комната 5
    elems_room5 = [
        'Кровать полуторная 120×200',
        'Стул деревянный складной',
        'Стол складной пластиковый',
        'Стол обеденный малый',
        'Унитаз напольный эконом',
        'Раковина угловая компакт',
    ]
    for name in elems_room5:
        elem = RoomElement.objects.get(name=name)
        RoomElementAssignment.objects.get_or_create(room=room5, element=elem)

    # ---------- СТАНДАРТ (комнаты 1,2,3) ----------
    # Обязательные: кровать, стол, стул, унитаз, раковина.
    # Опциональная техника – добавляем выборочно.

    # Комната 1
    elems_room1 = [
        # обязательные
        'Кровать двуспальная 160×200',
        'Стул офисный',
        'Стул эргономичный',
        'Стол письменный',
        'Стол журнальный',
        'Стол туалетный с зеркалом',
        'Унитаз подвесной',
        'Раковина прямоугольная',
        # опциональные
        'Телевизор LED 32"',
        'Радиоприемник портативный',
    ]
    for name in elems_room1:
        elem = RoomElement.objects.get(name=name)
        RoomElementAssignment.objects.get_or_create(room=room1, element=elem)

    # Комната 2
    elems_room2 = [
        'Кровать двуспальная 140×200',
        'Стул офисный',
        'Стул эргономичный',
        'Стол письменный',
        'Стол туалетный с зеркалом',
        'Унитаз напольный стандарт',
        'Раковина овальная керамика',
        # опциональные
        'Холодильник мини',
        'Телевизор LCD 24"',
    ]
    for name in elems_room2:
        elem = RoomElement.objects.get(name=name)
        RoomElementAssignment.objects.get_or_create(room=room2, element=elem)

    # Комната 3
    elems_room3 = [
        'Кровать двуспальная 140×200',
        'Стул офисный',
        'Стол письменный',
        'Стол журнальный',
        'Унитаз подвесной',
        'Раковина прямоугольная',
        # опциональные
        'Холодильник без морозилки',
        'Радиоприемник портативный',
    ]
    for name in elems_room3:
        elem = RoomElement.objects.get(name=name)
        RoomElementAssignment.objects.get_or_create(room=room3, element=elem)

    # ---------- ЛЮКС (комната 6) ----------
    elems_room6 = [
        # обязательные
        'Кровать King-size 200×200',
        'Кровать детская 90×180',
        'Стул кожаный Chesterfield',
        'Стул дизайнерский Eames',
        'Стол обеденный раздвижной',
        'Стол рабочий Executive',
        'Стол сервировочный',
        'Унитаз с биде-функцией',
        'Раковина двойная мраморная',
        # опциональные
        'Телевизор OLED 55"',
        'Холодильник мини-бар',
        'Кофеварка капсульная Nespresso',
        'Радиоприемник Hi-Fi Yamaha',
    ]
    for name in elems_room6:
        elem = RoomElement.objects.get(name=name)
        RoomElementAssignment.objects.get_or_create(room=room6, element=elem)

class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0006_seed_incompatibilities'),
    ]
    operations = [
        migrations.RunPython(seed_assignments),
    ]