from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from django.shortcuts import get_object_or_404
from .forms import RoomForm

def home(request):
    context = {}
    q = request.GET.get('q')  if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context['rooms'] = rooms
    context['topics'] = topics
    context['room_count'] = room_count
    return render(request, 'home.html', context)

def rooms(request, pk):
    context = {}
    room = get_object_or_404(Room, pk=pk)
    context['room'] = room
    return render(request, 'room.html', context)

def createRoom(request):
    context = {}
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context['form'] = form
    return render(request, 'room_form.html', context)


def updateRoom(request, pk):
    context = {}
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context['room'] = room
    context['form'] = form
    return render(request, 'room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})