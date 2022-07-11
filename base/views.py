from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:home')
    context = {'page': page}
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login_register.html', context)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, "Invalid password")

    return render(request, 'base/login_register.html', context)


def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
    else:
        messages.error(request, "An error occurred during registration")
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)
    pass


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) | Q(name__contains=q) | Q(description__contains=q) | Q(host__username__contains=q))
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_count_all = Room.objects.all().count()
    page_messages = Message.objects.all().order_by('-created')
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,'page_messages':page_messages,'room_count_all':room_count_all}
    return render(request, 'base/home.html', context)


def logoutUser(request):
    logout(request)
    return redirect('base:home')


def detail(request, pk):
    room: Room = Room.objects.get(id=pk)
    messagesList = room.message_set.all().order_by('created')
    participants = room.participants.all()
    context = {'room_messages': messagesList, 'room': room, 'participants': participants}

    if request.method == 'POST':
        Message.objects.create(
            body=request.POST.get('body'),
            user=request.user,
            room=room
        )
        room.participants.add(request.user)
        return redirect('base:detail', room.id)
    return render(request, 'base/roomDetail.html', context)


@login_required(login_url='base:login')
def createRoom(request):
    response = request.POST
    if request.method == 'POST':
        response = request.POST
        room = Room.objects.create(name=response['room_name'], topic=response['topic'], )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.host = request.user
            instance.save()
            return redirect('base:home')

    context = {}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='base:login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You do not own this room")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='base:login')
def deleteRoom(request, pk):
    room = Room.objects.get(pk=pk)
    if request.user != room.host:
        return HttpResponse("You do not own this room")
    if request.method == 'POST':
        room.delete()
        return redirect('base:home')
    context = {'obj': room}
    return render(request, 'base/deleteTemplate.html', context)


@login_required(login_url='base:login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not the owner of this message")
    if request.method == 'POST':
        message.delete()
        return redirect('base:home')
    context = {'obj': message}
    return render(request, 'base/deleteTemplate.html', context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    page_messages = user.message_set.all()
    room_count_all = Room.objects.all().count()
    context = {'user':user, 'rooms':rooms,'topics':topics,'page_messages':page_messages,'room_count_all':room_count_all}
    return render(request, 'base/user_profile.html',context)