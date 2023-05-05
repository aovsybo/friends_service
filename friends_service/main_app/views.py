from django.shortcuts import render
from .models import User


def get_friends_list(request):
    users = User.objects.all()
    return render(request, 'main_app/friends.html', {"users": users})


def show_start_page(request):
    return render(request, 'main_app/index.html')
