from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from apps.todos.models import ToDoList
from apps.todos.forms import ToDoListForm, ToDoUpdateForm


@login_required
def todo_list(request):
    todos = ToDoList.objects.filter(author=request.user)
    context = {
        'todos': todos,
    }
    return render(request, 'todos/todo_list.html', context=context)


@login_required
def todo_info(request, pk):

    todo = get_object_or_404(ToDoList, pk=pk, author=request.user)

    context = {
        'todo': todo
    }

    return render(request, 'todos/todo_info.html', context=context)


@login_required
def create_todo(request):

    form = ToDoListForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.author = request.user
        todo.save()
        return redirect('todos:todo_info', pk=todo.id)

    context = {
        'form': form,
    }

    return render(request, 'todos/create_todo.html', context=context)


@login_required
def update_todo(request, pk):

    todo = get_object_or_404(ToDoList, pk=pk, author=request.user)
    form = ToDoUpdateForm(request.POST or None, instance=todo)

    if form.is_valid():
        form.save()
        return redirect('todos:todo_info', pk=todo.id)

    context = {
        'form': form,
        'todo': todo,
    }

    return render(request, 'todos/update_todo.html', context=context)

