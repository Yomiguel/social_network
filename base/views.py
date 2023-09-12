from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Topic
from .forms import RoomForm


def loginPage(request):

    page = 'Login'

    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User ' + username + ' Does Not Exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return (redirect('Home'))
        else:
            messages.error(request, 'Username Or Password Does Not Match')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return (redirect('Home'))


def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'An Error Ocurred During Registration')
    return render(request, 'base/login_register.html', context)


@login_required(login_url='Login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='Login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='Login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here!')

    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    return render(request, 'base/delete.html', {'obj': room})
