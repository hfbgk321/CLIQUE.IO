from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Notifications, name = "show_notifications")
]