from django.db import migrations

def seed_incompatibilities(apps, schema_editor):
    RoomElement = apps.get_model('rooms', 'RoomElement')
    IncompatibleRoomElement = apps.get_model('rooms', 'IncompatibleRoomElement')

    # Эконом – две разные кровати и два разных стула не могут быть вместе
    bed_economy_1 = RoomElement.objects.get(name='Кровать односпальная 90×200')
    bed_economy_2 = RoomElement.objects.get(name='Кровать полуторная 120×200')
    chair_economy_1 = RoomElement.objects.get(name='Стул пластиковый')
    chair_economy_2 = RoomElement.objects.get(name='Стул деревянный складной')

    IncompatibleRoomElement.objects.get_or_create(
        element=bed_economy_1,
        incompatible_element=bed_economy_2
    )
    IncompatibleRoomElement.objects.get_or_create(
        element=chair_economy_1,
        incompatible_element=chair_economy_2
    )

    # Стандарт – две двуспальные кровати несовместимы; телевизор и холодильник тоже
    bed_std_1 = RoomElement.objects.get(name='Кровать двуспальная 160×200')
    bed_std_2 = RoomElement.objects.get(name='Кровать двуспальная 140×200')
    tv_std = RoomElement.objects.get(name='Телевизор LED 32"')
    fridge_std = RoomElement.objects.get(name='Холодильник мини')

    IncompatibleRoomElement.objects.get_or_create(
        element=bed_std_1,
        incompatible_element=bed_std_2
    )
    IncompatibleRoomElement.objects.get_or_create(
        element=tv_std,
        incompatible_element=fridge_std
    )

    # Люкс – King-size несовместим с Queen-size; тостер с кофеваркой
    bed_lux_1 = RoomElement.objects.get(name='Кровать King-size 200×200')
    bed_lux_2 = RoomElement.objects.get(name='Кровать Queen-size 180×200')
    toaster_lux = RoomElement.objects.get(name='Тостер премиум Smeg')
    coffee_lux = RoomElement.objects.get(name='Кофеварка капсульная Nespresso')

    IncompatibleRoomElement.objects.get_or_create(
        element=bed_lux_1,
        incompatible_element=bed_lux_2
    )
    IncompatibleRoomElement.objects.get_or_create(
        element=toaster_lux,
        incompatible_element=coffee_lux
    )

class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0005_seed_room_elements'),
    ]
    operations = [
        migrations.RunPython(seed_incompatibilities),
    ]