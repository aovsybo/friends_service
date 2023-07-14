from typing import Literal

from django.shortcuts import render,  redirect
from django.contrib import messages
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import *


class FriendsListView(generics.ListAPIView):
    serializer_class = FriendsListSerializer
    queryset = User.objects.all()


class RequestsListView(generics.ListAPIView):
    serializer_class = FriendsListSerializer

    def get_queryset(self):
        user = self.request.user
        type_: Literal['incoming'] | Literal['outcoming'] | None = self.kwargs.get('type_')
        if type_ == 'outcoming':
            return user.outcoming_requests.all()
        if type_ == 'incoming':
            return user.incoming_requests.all()
        return user.incoming_requests.all() | \
               user.outcoming_requests.all()


class SendRequestAPIView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SendRequestSerializer

    def post(self, request):
        super().create(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


def find_friends(request):
    users = User.objects.all()
    return render(request, 'main_app/find_friends.html', {"users": users})


def remove_friend(request, user_id):
    request.user.friends.remove(user_id)
    messages.success(request, 'Friend deleted')
    return redirect('friends')


@transaction.atomic
def add_friends_to_each_other(friend_request):
    friend_request.to_user.friends.add(friend_request.from_user)
    friend_request.delete()


def get_users(request):
    users = User.objects.all()
    return render(request, 'main_app/users.html', {"users": users, "status": ""})


def get_status(request, user_id):
    current_user = request.user
    checking_user = User.objects.get(id=user_id)
    # request_status = FriendRequest.objects.filter(
    #     Q(from_user_id=request.user.id, to_user_id=user_id) |
    #     Q(from_user_id=user_id, to_user_id=request.user.id) |
    #     Q(is_approved=True)
    # )
    # is_approved - friends
    # user == from_user - 1
    # user == to_user - 2
    # else - 3
    if current_user.friends.contains(checking_user):
        status = f"You are friends with {checking_user}"
    elif FriendRequest.objects.filter(
            from_user=current_user,
            to_user=checking_user
    ).exists():
        status = f"You sent friend request to {checking_user}"
    elif FriendRequest.objects.filter(
            from_user=checking_user,
            to_user=current_user
    ).exists():
        status = f"{checking_user} sent friend request to you"
    else:
        status = f"You are not friends with {checking_user}"
    return render(request, 'main_app/users.html', {"status": status})


def accept_request(request, request_id):
    # TODO:
    #  get_object_or_404 - drf
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
