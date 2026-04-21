from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, RoomElement
from .forms import RoomForm


def index(request):
    return (render(request, "index.html"))


def rooms(request):
    rooms_qs = Room.objects.all()
    context = {
        "rooms": rooms_qs
    }
    return render(request, "rooms.html", context)


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    elements = RoomElement.objects.filter(room_id=room)
    context = {
        "room": room,
        "elements": elements
    }
    return render(request, "room_detail.html", context)


def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:rooms')
    else:
        form = RoomForm()
    context = {
        'form': form,
        'title': 'Добавить комнату'
    }
    return render(request, 'room_form.html', context)


def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms:rooms')
    else:
        form = RoomForm(instance=room)
    context = {
        'form': form,
        'title': f'Изменить комнату {room.id}'
    }
    return render(request, 'room_form.html', context)


def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('rooms:rooms')
    context = {
        'room': room
    }
    return render(request, 'room_confirm_delete.html', context)


def elements(request):
    elements_qs = RoomElement.objects.all()
    context = {
        "elements": elements_qs
    }
    return render(request, "elements.html", context)


def element_create(request):
    if request.method == 'POST':
        from .forms import RoomElementForm
        form = RoomElementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:elements')
    else:
        from .forms import RoomElementForm
        form = RoomElementForm()
    context = {
        'form': form,
        'title': 'Добавить предмет'
    }
    return render(request, 'element_form.html', context)


def element_update(request, pk):
    from .forms import RoomElementForm
    element = get_object_or_404(RoomElement, pk=pk)
    if request.method == 'POST':
        form = RoomElementForm(request.POST, instance=element)
        if form.is_valid():
            form.save()
            return redirect('rooms:elements')
    else:
        form = RoomElementForm(instance=element)
    context = {
        'form': form,
        'title': f'Изменить предмет {element.name}'
    }
    return render(request, 'element_form.html', context)


def element_delete(request, pk):
    element = get_object_or_404(RoomElement, pk=pk)
    if request.method == 'POST':
        element.delete()
        return redirect('rooms:elements')
    context = {
        'element': element
    }
    return render(request, 'element_confirm_delete.html', context)


def incompatible_elements(request):
    from .models import IncompatibleRoomElement
    incompatible_qs = IncompatibleRoomElement.objects.all()
    context = {
        "incompatible_elements": incompatible_qs
    }
    return render(request, "incompatible_elements.html", context)


def incompatible_create(request):
    from .forms import IncompatibleRoomElementForm
    if request.method == 'POST':
        form = IncompatibleRoomElementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:incompatible_elements')
    else:
        form = IncompatibleRoomElementForm()
    context = {
        'form': form,
        'title': 'Добавить несовместимость'
    }
    return render(request, 'incompatible_form.html', context)


def incompatible_update(request, pk):
    from .forms import IncompatibleRoomElementForm
    from .models import IncompatibleRoomElement
    incompatible = get_object_or_404(IncompatibleRoomElement, pk=pk)
    if request.method == 'POST':
        form = IncompatibleRoomElementForm(request.POST, instance=incompatible)
        if form.is_valid():
            form.save()
            return redirect('rooms:incompatible_elements')
    else:
        form = IncompatibleRoomElementForm(instance=incompatible)
    context = {
        'form': form,
        'title': 'Изменить несовместимость'
    }
    return render(request, 'incompatible_form.html', context)


def incompatible_delete(request, pk):
    from .models import IncompatibleRoomElement
    incompatible = get_object_or_404(IncompatibleRoomElement, pk=pk)
    if request.method == 'POST':
        incompatible.delete()
        return redirect('rooms:incompatible_elements')
    context = {
        'incompatible': incompatible
    }
    return render(request, 'incompatible_confirm_delete.html', context)


def generate_room_elements(request, pk):
    room = get_object_or_404(Room, pk=pk)
    context = {
        'room': room
    }
    return render(request, 'generate_room_elements.html', context)
