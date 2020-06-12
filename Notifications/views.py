from django.shortcuts import render
import datetime
from .models import NotificationModel

# Create your views here.

def Notifications(request):
  all_notifications = NotificationModel.objects.filter(account=request.user)
  return all_notifications
  #return render(request,'authorize_main/base.html',{"all_notifications":all_notifications})

