from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout



def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:login')

    context = {'form': form}

    return render(request, 'registration/signup.html', context=context)


def login(request):

    form = AuthenticationForm(request=request, data=request.POST or None)

    if form.is_valid():
        dj_login(request, form.get_user())
        return redirect('todo_list')

    context = {'form': form}

    return render(request, 'registration/login.html', context=context)


def logout(request):

    dj_logout(request)

    return redirect('todo_list')