from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from django.shortcuts import get_object_or_404
from .forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
             
    context = {}
    return render(request,'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})