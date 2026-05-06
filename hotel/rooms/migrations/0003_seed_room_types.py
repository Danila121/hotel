from django.db import migrations

def seed_room_types(apps, schema_editor):
    RoomType = apps.get_model('rooms', 'RoomType')
    for name in ["Стандарт", "Эконом", "Люкс"]:
        RoomType.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0002_seed_element_types'),
    ]
    operations = [
        migrations.RunPython(seed_room_types),
    ]