from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Notifications, name = "show_notifications"),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name ='delete_notification'),
]