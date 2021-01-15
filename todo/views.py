from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from todo.models import Todo
from todo.templates.todo.forms import TodoForm


def home(request):
    return render(request, 'todo/home.html')


def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'todo/sign_up_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(current_todos)
            except IntegrityError:
                return render(request, 'todo/sign_up_user.html',
                              {'form': UserCreationForm(), 'error': 'That username is already taken !!'})
        else:
            return render(request, 'todo/sign_up_user.html', {'form': UserCreationForm(), 'error': 'Passwords did not match !'})


@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/current_todos.html', {'todos': todos})


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completed_todos.html', {'todos': todos})


def login_user(request):

    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html', {'form': AuthenticationForm(), 'error': 'username and password did not match'})
        else:
            login(request, user)
            return redirect('current_todos')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todos(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todos.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todos.html', {'form': TodoForm(), 'error': 'Bad data passed in'})


@login_required
def views_todos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/views_todos.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/views_todos.html', {'todo': todo, 'form': form, 'error': 'Bad infos'})


@login_required
def complete_todos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required
def delete_todos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')
