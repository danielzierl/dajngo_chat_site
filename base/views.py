from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    print(q)
    rooms = Room.objects.filter(Q(topic__name__contains=q) | Q(name__contains=q)| Q(description__contains=q))
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics,'room_count':room_count}
    return render(request, 'base/home.html', context)


def detail(request, pk):
    return HttpResponse('Not impemented yet')

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:home')
    context = {'form':form}
    return render(request, 'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method=='POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:home')
    context = {'form':form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('base:home')
    context = {'obj':room}
    return render(request, 'base/deleteTemplate.html',context)