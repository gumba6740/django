from django.shortcuts import render
from django.http import Http404


def gugudan(request):
    numbers = [i for i in range(1,10)]

    return render(request, 'gugu.html', {'numbers':numbers})


def gugudan2(request, number):
    if number > 9:
        raise Http404

    numbers = [number * result for result in range(1,10)]

    return render(request, 'gugu2.html', {'number':number, 'numbers': numbers})
