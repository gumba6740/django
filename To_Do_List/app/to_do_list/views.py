from django.http import Http404
from django.shortcuts import render
from app.to_do_list.models import ToDoList


def todo_list(request):
    todos = ToDoList.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'todo_list.html', context=context)


def todo_info(request, todo_id):

    try:
        todo = ToDoList.objects.get(id=todo_id)
    except:
        raise Http404

    context = {
        'todo': todo
    }

    return render(request, 'todo_info.html', context=context)