from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
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
            user.username = user.username
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
    room_comments = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_comments': room_comments
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        publish_comment = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return (redirect('Room', pk=room.id))

    context = {
        'room': room,
        'comments': comments,
        'participants': participants
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room = form.save()
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


@login_required(login_url='Login')
def deleteComment(request, pk):
    comment = Message.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You Are Not Allowed Here!')

    if request.method == 'POST':
        comment.delete()
        return redirect('Home')
    return render(request, 'base/delete.html', {'obj': comment})


def userProfile(request, pk):

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_comments = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_comments': room_comments,
        'topics': topics
    }
    return render(request, 'base/profile.html', context)