from django.urls import path

from . import views


urlpatterns = [
    path('', views.show_start_page, name="main"),
    path('friends', views.get_friends_list, name="friends"),
]
