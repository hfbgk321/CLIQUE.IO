from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_chat_room, name='main_chat_room'), #beta chat link
    path('<str:room_name>/', views.room, name='room'), #final chat link
    path('change_chat_name/<str:chat_url>/', views.change_chat_room, name='change_chat_room'),
    path('friend_chat/<int:other_id>/', views.friend_chat, name='friend_chat'),
]