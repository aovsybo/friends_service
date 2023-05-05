from django.urls import path

from . import views


urlpatterns = [
    path('', views.show_start_page, name="main"),
    path('friends', views.get_friends_list, name="friends"),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('sign_up/', views.sign_up, name='sign_up'),
]
