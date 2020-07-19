from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current')
            except IntegrityError:
                return render(request, 'todo/signup.html',
                              {'form': UserCreationForm(),
                               'error': 'This username has already been taken. Please choose new username'})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'Username or Password doesnt match'})
        else:
            login(request, user)
            return redirect('current')




def currentuser(request):
    todo = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/current.html', {'todos': todo})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': TodoForm()})
    else:
        try:
           form = TodoForm(request.POST)
           newTodo = form.save(commit=False)
           newTodo.user = request.user
           newTodo.save()
           return redirect('current')
        except ValueError:
            return render(request, 'todo/create.h   tml', {'form': TodoForm(), 'error': 'Bad data passed in'})

@login_required
def viewtodo(request, pk):
    todo = get_object_or_404(Todo,id=pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:

        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error':'Bad data passed in'})


@login_required
def completetodo(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('current')

@login_required
def deletetodo(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')

@login_required
def completed(request):
    todo = Todo.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completed.html', {'todos': todo})

