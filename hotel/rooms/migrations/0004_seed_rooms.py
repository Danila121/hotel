from django.db import migrations

def seed_rooms(apps, schema_editor):
    Room = apps.get_model('rooms', 'Room')
    RoomType = apps.get_model('rooms', 'RoomType')

    standard = RoomType.objects.get(name="Стандарт")
    economy = RoomType.objects.get(name="Эконом")
    luxury = RoomType.objects.get(name="Люкс")

    rooms = [
        (standard, 1),
        (standard, 2),
        (standard, 3),
        (economy, 4),
        (economy, 5),
        (luxury, 6),
    ]
    for room_type, room_id in rooms:
        Room.objects.get_or_create(
            id=room_id,
            room_type=room_type,
        )

class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0003_seed_room_types'),
    ]
    operations = [
        migrations.RunPython(seed_rooms),
    ]