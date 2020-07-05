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
    
    check = NotificationModel.objects.filter(account=friend, url='verify_friend', data = [user.id], notified_message =f'{user.first_name} {user.last_name} wants to be your friend!')
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
        
    notification = NotificationModel.objects.filter(account=Account.objects.get(id=request.user.id), url='verify_friend', data=[friend_id])
    for x in notification:
        x.delete()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def reject_friend(request, friend_id):
    notification = NotificationModel.objects.filter(account=Account.objects.get(id=request.user.id), url='verify_friend', data=[friend_id])
    for x in notification:
        x.delete()
    
    user = Account.objects.get(id=request.user.id)
    
    messages.success(request, 'Friend Request Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_friend(request, friend_id):
    friend = Account.objects.get(id=friend_id)
    user = Account.objects.get(id=request.user.id)
            
    for id_check in range(len(user.friends)):
        if user.friends[id_check] == friend.id:
            user.friends.pop(id_check)
            user.save()
            
    for id_check in range(len(friend.friends)):
        if friend.friends[id_check] == user.id:
            friend.friends.pop(id_check)
            friend.save()
    messages.success(request, 'Friend Sucessfully Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def friend_search(request):
    user = Account.objects.get(id=request.user.id)
    user_settings = user.show_to_public
    
    relevant_friends = []
    print(">>>>>>>", request.POST)
    friend_name = request.POST['search_friend_name'].strip().split()
    
    for friend_id in user.friends:
        friend = Account.objects.get(id=friend_id)
        
        for part in range(len(friend_name)):
            if friend_name[part].lower() in friend.first_name.lower():
                relevant_friends.append(friend)
                break
            elif friend_name[part].lower() in friend.last_name.lower():
                relevant_friends.append(friend)
                break
    
    return render(request,'authorize_main/new_profile.html', {'friend_list': relevant_friends,'profile_pic': user_settings[0], 'email': user_settings[1],'first_name': user_settings[2], 'last_name': user_settings[3],'university': user_settings[4], 'major': user_settings[5],'school_year': user_settings[6], 'date_joined': user_settings[7],"all_notifications":Notifications(request)})
 
def get_mutual_friends(request):
    user = Account.objects.get(id=request.user.id)
    user_friends = user.friends
    
    mutual_friends = []

    
    for friend in user_friends:
        friend = Account.objects.get(id=friend)
        
        for friend2 in friend.friends:
            if friend2 != request.user.id and friend2 in user.friends and friend2 != friend.id:
                if Account.objects.get(id=friend2) not in mutual_friends:
                    mutual_friends.append(Account.objects.get(id=friend2))

    return mutual_friends