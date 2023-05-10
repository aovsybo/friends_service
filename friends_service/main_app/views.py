from django.shortcuts import render,  redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm
from .models import FriendRequest, User


def get_friends_list(request):
    friends = request.user.friends.all()
    return render(request, 'main_app/friends.html', {"friends": friends})


def get_users_list(request):
    users = User.objects.all()
    return render(request, 'main_app/users.html', {"users": users})


def get_requests(request):
    friend_requests = FriendRequest.objects.all()
    return render(request, 'main_app/requests.html', {"friend_requests": friend_requests})


def remove_friend(request, user_id):
    friend = User.objects.get(id=user_id)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)
    messages.success(request, 'Friend deleted')
    return redirect('friends')


def send_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    if FriendRequest.objects.filter(
        from_user=to_user,
        to_user=from_user
    ).exists():
        prev_friend_request = FriendRequest.objects.get(
            from_user=to_user,
            to_user=from_user
        )
        add_friends_to_each_other(prev_friend_request)
        messages.success(request, 'Friendship accepted')
        return redirect('friends')
    friend_request, is_created = FriendRequest.objects.get_or_create(
        from_user=from_user,
        to_user=to_user
    )
    if is_created:
        messages.success(request, 'Request sent')
        return redirect('main')
    else:
        messages.success(request, 'Request already exists')
        return redirect('main')


def add_friends_to_each_other(friend_request):
    friend_request.to_user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.delete()


def accept_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        add_friends_to_each_other(friend_request)
        messages.success(request, 'Friendship accepted')
        return redirect('friends')


def decline_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.success(request, 'Friendship declined')
        return redirect('friends')


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
