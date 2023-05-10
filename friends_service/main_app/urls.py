from django.urls import path
from django.contrib import admin

from . import views


urlpatterns = [
    path('', views.show_start_page, name="main"),
    path('friends', views.get_friends_list, name="friends"),
    path('admin', admin.site.urls, name="admin"),
    # path('remove_friend/<int:id>', views.remove_friend, name="remove_friend"),
    # path('add_friend/<int:id>', views.add_friend, name="add_friend"),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('sign_up', views.sign_up, name='sign_up'),
]
