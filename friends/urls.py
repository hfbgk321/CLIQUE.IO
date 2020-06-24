from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('add_friend/<int:applicant_id>/', views.add_friend, name ='add_friend'),
    path('add_friend/', views.add_friend, name ='add_friend'),
    
]