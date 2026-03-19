from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login
from django.conf import settings



def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    context = {'form': form}

    return render(request, 'registration/signup.html', context=context)


def login(request):

    form = AuthenticationForm(request=request, data=request.POST or None)

    if form.is_valid():
        dj_login(request, form.get_user())
        next = request.GET.get('next')

        if next:
            return redirect(next)

        return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'form': form}

    return render(request, 'registration/login.html', context=context)

