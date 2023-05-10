from django.urls import path
from django.contrib import admin

from . import views


urlpatterns = [
    path('', views.show_start_page, name="main"),
    path('find_friends', views.find_friends, name="find_friends"),
    path('friends', views.get_friends_list, name="friends"),
    path('requests', views.get_requests, name="requests"),
    path('remove_friend/<int:user_id>', views.remove_friend, name="remove_friend"),
    path('send_request/<int:user_id>', views.send_request, name="send_request"),
    path('users', views.get_users, name="users"),
    path('get_status/<int:user_id>', views.get_status, name="get_status"),
    path('accept_request/<int:request_id>', views.accept_request, name="accept_request"),
    path('decline_request/<int:request_id>', views.decline_request, name="decline_request"),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('sign_up', views.sign_up, name='sign_up'),
]
