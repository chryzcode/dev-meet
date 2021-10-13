from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from django.shortcuts import get_object_or_404
from .forms import RoomForm, UserForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
             
    context = {'page':page}
    return render(request,'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = SignupForm
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'login_register.html', {'form':form})

def home(request):
    context = {}
    q = request.GET.get('q')  if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context['rooms'] = rooms
    context['topics'] = topics
    context['room_count'] = room_count
    context['room_messages'] = room_messages
    return render(request, 'home.html', context)

def rooms(request, pk):
    context = {}
    room = get_object_or_404(Room, pk=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context['room'] = room
    context['room_messages'] = room_messages
    context['participants'] = participants
    return render(request, 'room.html', context)

def userProfile(request, username):
    context = {}
    user = get_object_or_404(User, username=username)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context['user'] = user
    context['rooms'] = rooms
    context['room_messages'] = room_messages
    context['topics'] = topics
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    context = {}
    form = RoomForm
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic, 
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    context['form'] = form
    context['topics'] = topics
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    context = {}
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = request.POST.get('topic')
        room.description = request.POST.get('description')
        return redirect('home')
    context['room'] = room
    context['form'] = form
    context['topics'] = topics
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request, username):
    context = {}
    user = get_object_or_404(User, username=username)
    form = UserForm(instance= request.user)  
    if request.method == 'POST':
        form = UserForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save() 
            return redirect('user-profile', username)
    context['form'] = form
    return render(request, 'update_user.html', context)

def topicsPage(request):
    context = {}
    q = request.GET.get('q')  if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context['topics'] = topics
    return render(request, 'topics.html', context)

def activityPage(request):
    context = {}
    room_messages = Message.objects.all()
    context['room_messages'] = room_messages
    return render(request, 'activity.html', context)