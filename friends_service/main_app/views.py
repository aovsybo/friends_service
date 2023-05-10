from django.shortcuts import render,  redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm


def get_friends_list(request):
    # TODO: get friends, not users
    friends = User.objects.all()
    return render(request, 'main_app/friends.html', {"friends": friends})


def show_start_page(request):
    return render(request, 'main_app/index.html')


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd["username"],
                password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Signed in')
                    return redirect('main')
                else:
                    messages.success(request, 'Disabled account')
            else:
                messages.success(request, 'Invalid login')
    else:
        form = LoginForm(request.POST)
    return render(request, 'main_app/sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('main')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'main_app/sign_up.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Signed up')
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'main_app/sign_up.html', {'form': form})
