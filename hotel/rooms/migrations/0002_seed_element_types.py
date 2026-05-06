from django.db import migrations

def seed_element_types(apps, schema_editor):
    ElementType = apps.get_model('rooms', 'ElementType')
    types = [
        ("Кровать", True),
        ("Стол", True),
        ("Стул", True),
        ("Унитаз", True),
        ("Раковина", True),
        ("Радиоприемник", False),
        ("Телевизор", False),
        ("Холодильник", False),
        ("Кофеварка", False),
        ("Тостер", False),
    ]
    for name, is_required in types:
        ElementType.objects.create(name=name, is_required=is_required)

class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_element_types),
    ]