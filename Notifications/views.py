from django.shortcuts import render,redirect
import datetime
from django.contrib import messages
from .models import NotificationModel

# Create your views here.

def Notifications(request): #returns all notification relating to user in time order
  all_notifications = NotificationModel.objects.filter(account=request.user).order_by('date_created').reverse()
 
  return all_notifications
  

def delete_notification(request, notification_id):
  notification = NotificationModel.objects.get(id=notification_id)
  notification.delete()
  messages.success(request,'Notification successfully deleted')
  return redirect(request.META['HTTP_REFERER'], '/')

#debug

def delete_all_notifications(request):
  
  notification = NotificationModel.objects.filter(account__id=request.user.id)
  for notif in notification:
    notif.delete()
  return redirect('hometemplate')

def list_all_people():
    all_people = Account.objects.all()
    return all_people
  