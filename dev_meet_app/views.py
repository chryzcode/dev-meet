from django.shortcuts import render
from .models import Room
from django.shortcuts import get_object_or_404

def home(request):
    context = {}
    rooms = Room.objects.all()
    context['rooms'] = rooms
    return render(request, 'home.html', context)

def rooms(request, pk):
    context = {}
    room = get_object_or_404(Room, pk=pk)
    context['room'] = room
    return render(request, 'room.html', context)