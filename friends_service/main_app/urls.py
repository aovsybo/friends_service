from django.urls import path
from django.contrib import admin

from . import views


urlpatterns = [
    path('', views.FriendsListView.as_view()),
    path('requests/', views.RequestsListView.as_view()),
    path('send_request/', views.SendRequestAPIView.as_view()),

    path('users', views.get_users, name="users"),
    path('find_friends', views.find_friends, name="find_friends"),
    path('remove_friend/<int:user_id>', views.remove_friend, name="remove_friend"),
    path('get_status/<int:user_id>', views.get_status, name="get_status"),
    path('accept_request/<int:request_id>', views.accept_request, name="accept_request"),
    path('decline_request/<int:request_id>', views.decline_request, name="decline_request"),
]
