from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('send_friend_request/<int:applicant_id>/', views.send_friend_request, name ='send_friend_request'),
    path('send_friend_request/', views.send_friend_request, name ='send_friend_request'),
    path('view_friends/', views.view_friend_page, name='view_friend_page'),
    path('accept_friend/<int:friend_id>/', views.accept_friend, name= 'accept_friend'),
    path('reject_friend/<int:friend_id>/', views.reject_friend, name= 'reject_friend'),
    path('verify_friend/<int:friend_id>/', views.verify_friend, name = 'verify_friend'),
    path('verify_friend/', views.verify_friend, name = 'verify_friend'),
    path('delete_friend/<int:friend_id>/', views.delete_friend, name = 'delete_friend'),
    path('friend_search/', views.friend_search, name='friend_search'),
]