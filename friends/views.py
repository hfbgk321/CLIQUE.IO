from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from authorize_main.models import Account
from Notifications.views import Notifications
from Notifications.models import NotificationModel

# Create your views here.

def add_friend(request, applicant_id):
    print(applicant_id)
    user = Account.objects.get(id=request.user.id)
    friend = Account.objects.get(id= applicant_id)
    friend.friends.append(user.id)
    user.friends.append(applicant_id)
    
    notification = NotificationModel.objects.create(account=user, notified_message =f'{Account.objects.get(id=applicant_id).first_name} {Account.objects.get(id=applicant_id).last_name} wants to be your friend!')
    notification.save()

    return HttpResponse(applicant_id)
