from django.shortcuts import render, get_object_or_404
from .models import Room, RoomElement, RoomElementAssignment, IncompatibleRoomElement
from .forms import ElementSelectionForm
from django.db.models import Count, Q


def index(request):
    return render(request, "index.html")


def rooms(request):
    rooms_qs = Room.objects.all()
    context = {
        "rooms": rooms_qs
    }
    return render(request, "rooms.html", context)


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    assignments = RoomElementAssignment.objects.filter(room=room)
    elements = [assignment.element for assignment in assignments]
    context = {
        "room": room,
        "elements": elements,
        "assignments": assignments,
    }
    return render(request, "room_detail.html", context)


def elements(request):
    elements_qs = RoomElement.objects.all()
    context = {
        "elements": elements_qs
    }
    return render(request, "elements.html", context)


def incompatible_elements(request):
    incompatible_qs = IncompatibleRoomElement.objects.all()
    context = {
        "incompatible_elements": incompatible_qs
    }
    return render(request, "incompatible_elements.html", context)


def select_room(request):
    form = ElementSelectionForm()
    results = None
    perfect = False

    if request.method == 'POST':
        form = ElementSelectionForm(request.POST)
        if form.is_valid():
            selected_elements = form.cleaned_data['elements']
            total_requested = len(selected_elements)

            # Аннотируем каждую комнату количеством выбранных элементов в ней
            rooms_with_counts = Room.objects.annotate(
                matches=Count('roomelementassignment__element',
                    filter=Q(roomelementassignment__element__in=selected_elements))
            )

            # Проверяем, есть ли комнаты со 100% совпадением
            exact_rooms = rooms_with_counts.filter(matches=total_requested)
            if exact_rooms.exists():
                perfect = True
                results = [(room, 100.0) for room in exact_rooms]
            else:
                perfect = False
                # Отбираем комнаты с ненулевым совпадением, считаем процент
                rooms_with_matches = rooms_with_counts.filter(matches__gt=0)
                temp = []
                for room in rooms_with_matches:
                    percent = (room.matches / total_requested) * 100
                    temp.append((room, percent))
                # Сортируем по убыванию процента
                temp.sort(key=lambda x: x[1], reverse=True)
                top3 = temp[:3]
                results = [(room, round(percent, 1)) for room, percent in top3]

    return render(request, 'select_room.html', {
        'form': form,
        'results': results,
        'perfect': perfect,
    })