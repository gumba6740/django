from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.todo.models import ToDo
from apps.todo.forms import ToDoForm, ToDoUpdateForm


@login_required
def todo_list(request):
    todos = ToDo.objects.filter(user=request.user).order_by('end_date')

    q = request.GET.get('q')
    if q:
        todos = todos.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
    paginator = Paginator(todos, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'todo/todo_list.html', context=context)


@login_required
def todo_info(request, pk):

    todo = get_object_or_404(ToDo, pk=pk, user=request.user)

    context = {
        'todo': todo
    }

    return render(request, 'todo/todo_info.html', context=context)


@login_required
def create_todo(request):

    form = ToDoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect('todo:info', pk=todo.id)

    context = {
        'form': form,
    }

    return render(request, 'todo/create_todo.html', context=context)


@login_required
def update_todo(request, pk):

    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    form = ToDoUpdateForm(request.POST or None, instance=todo)

    if form.is_valid():
        form.save()
        return redirect('todo:info', pk=todo.id)

    context = {
        'form': form,
        'todo': todo,
    }

    return render(request, 'todo/update_todo.html', context=context)


@login_required
@require_http_methods(['POST'])
def delete_todo(request, pk):

    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    todo.delete()

    return redirect('todo:list')
