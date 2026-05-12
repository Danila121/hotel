from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import HotelRoomType, HotelRoomElement, ElementSort, IncompatibleRoomElement
from .engine import get_allowed_elements
import json


def index(request):
	room_types = HotelRoomType.objects.all()
	types_data = []
	for rt in room_types:
		elements = HotelRoomElement.objects.filter(room_type=rt).select_related("element_sort")
		sorts_dict = {}
		for el in elements:
			sort_name = el.element_sort.name
			if sort_name not in sorts_dict:
				sorts_dict[sort_name] = {
					"name": sort_name,
					"is_required": el.element_sort.is_required,
					"elements": [],
				}
			sorts_dict[sort_name]["elements"].append({
				"name": el.name,
				"id": el.pk,
			})
		
		incompat = IncompatibleRoomElement.objects.filter(
			element__room_type=rt
		).select_related("element", "incompatible_element")
		incompat_list = [[inc.element.name, inc.incompatible_element.name] for inc in incompat]

		types_data.append({
			"room_type": rt.name,
			"sorts": list(sorts_dict.values()),
			"incompatibilities": incompat_list,
		})

	context = {
		"room_types": room_types,
		"types_data_json": json.dumps(types_data, ensure_ascii=False),
	}
	return render(request, "index.html", context)


def generate_variants(request):
	"""
	Принимает POST с JSON:
	{
		"room_type": "Стандарт",
		"selected": [
			{"element": "Кровать МОРИ ЛЮКС", "quantity": 2},
			...
		]
	}
	Возвращает список допустимых комбинаций.
	"""
	if request.method != "POST":
		return JsonResponse({"error": "POST required"}, status=405)

	try:
		body = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({"error": "Invalid JSON"}, status=400)

	room_type = body.get("room_type")
	selected = body.get("selected", [])

	if not room_type:
		return JsonResponse({"error": "room_type is required"}, status=400)

	result = get_allowed_elements(room_type, selected)

	return JsonResponse({"variants": result})