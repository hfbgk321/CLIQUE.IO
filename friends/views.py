from django.shortcuts import render,redirect, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from authorize_main.models import Account
from Notifications.views import Notifications
from Notifications.models import NotificationModel
from django.contrib import messages

# Create your views here.

def send_friend_request(request, applicant_id):
    user = Account.objects.get(id=request.user.id)
    friend = Account.objects.get(id= applicant_id)
    
    check = NotificationModel.objects.filter(account=friend, url='verify_friend', data = [str(user.id)], notified_message =f'{user.first_name} {user.last_name} wants to be your friend!')
    if len(check) == 0:
        notification = NotificationModel.objects.create(account=friend, url='verify_friend', data = [str(user.id)], notified_message =f'{user.first_name} {user.last_name} wants to be your friend!')
    messages.success(request, 'Friend Request Sucessfully Sent')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def view_friend_page(request):
    user = Account.objects.get(id=request.user.id)
    friends_id = user.friends
    friends_names = []
    
    for friend_id in friends_id:
        friend = Account.objects.get(id=friend_id)
        friends_names.append(friend.first_name)

    return render(request, 'friends/friends_main.html', {'friends_names': friends_names, 'all_notifications': Notifications(request)}) 
    
def verify_friend(request, friend_id):
    friend_id = int(friend_id)
    user = Account.objects.get(id=request.user.id)
    friend = Account.objects.get(id=friend_id)

    return render(request, 'friends/verify_friend.html', {'friend': friend, 'all_notifications': Notifications(request)})

def accept_friend(request, friend_id):
    user = Account.objects.get(id=request.user.id)
    friend = Account.objects.get(id= friend_id)
    if user.id not in friend.friends:
        friend.friends.append(user.id)
        friend.save()
        user.friends.append(friend_id)
        user.save()
        messages.success(request, 'Friend Successfully Added')
    else:
        messages.success(request, 'Friend Already Added')
    return redirect('view_friend_page')

def reject_friend(request, friend_id):
    notification = NotificationModel.objects.filter(account=Account.objects.get(id=request.user.id), url='verify_friend')
    for x in notification:
        x.delete()

    user = Account.objects.get(id=request.user.id)
    
    messages.success(request, 'Friend Request Deleted')
    return redirect('view_friend_page')