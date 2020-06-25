# chat/views.py
from django.shortcuts import render, redirect
from authorize_main.models import Account
from Notifications.models import NotificationModel
from authorize_main.models import Account
from .models import ChatModel
import random
from django.http import HttpResponse
from django import template
import urllib

register = template.Library()

#from chat.views import chat_key_seeder, create_private_chat, notify_chat, url_scrambler

def main_chat_room(request):
    user = Account.objects.get(id=request.user.id)
    chats = []
    for key in user.chat_keys:
        check = ChatModel.objects.filter(key=key)
        
        for x in check:
            chats.append(x)
    
    return render(request, 'chat/index.html', {'user': user, 'friends':user.friends, 'chats':chats})

def room(request, room_name):
    other_guy = ''
    user = Account.objects.get(id=request.user.id)#created_by
    user_name = user.first_name
    message_combined = ['']
    room_model = ChatModel.objects.filter(url=room_name)
    
    #verify
    if verify_chat_member(request, room_name) == True or True:
        text_log, lr_arr, message_combined = load_chat_log(request, room_name)
        #message_combined = zip(text_log,lr_arr)
        #print(message_combined)
        room_model = ChatModel.objects.get(url=room_name)
        
        id_arr = room_model.users
        #print(id_arr)
        for x in id_arr:
            person = Account.objects.get(id=x)
            print(person.id)
            print(user.id)
            if person.id != user.id:
                other_guy = person
            #else:
                #other_guy = person
        
        img_src = other_guy.profile_pic.url
        user_img = user.profile_pic.url
        
        #print(room_model.chat_name)
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'user': user,
            #'message_combined': message_combined,
            'room_model': room_model,
            #'text_log': text_log, 
            #'lr_arr': lr_arr,
            "message_combined":message_combined,
            "img_src":img_src,
            "user_img":user_img,
            "friends":list_all_people()
        })
    else:
        return HttpResponse('Account Denied')

@register.filter
def zip_lists(a, b):
  return zip(a, b)

def notify_chat(request, user_id, applicant_id=0):
    notification = NotificationModel.objects.create(account=request.user,notified_message =f'{Account.objects.get(id=user_id).first_name} {Account.objects.get(id=user_id).last_name} wants to chat!')
    notification.save()

def create_private_chat(request, room_name, second_person_id=None, id_arr=None):
    creator = Account.objects.get(id=request.user.id)
    
    room_model = ChatModel.objects.filter(url=room_name)

    if second_person_id:
        second_person = Account.objects.get(id=second_person_id)
        key = chat_key_seeder(request.user.id, second_person_id)
        #print(room_name, request.user.id, second_person_id, key)
        if len(room_model) == 0:
            #print(creator.chat_keys, second_person.chat_keys)
            
            ChatModel.objects.create(users=[request.user.id, second_person_id], owner=creator.id, url=room_name, chat_name=creator.first_name + "'s Chat", messages=[''], key=key)
            room_model = ChatModel.objects.get(url=room_name)
            print(room_model.users)
            if key not in creator.chat_keys:
                #print('creator', creator.first_name)
                creator.chat_keys.append(key)
                creator.save()
            if key not in second_person.chat_keys:
                second_person.chat_keys.append(key)
                second_person.save()
            #print(room_name)
            notify_chat(request, request.user.id)
            return ChatModel.objects.get(url=room_name)
            
        else: 
            room_model = ChatModel.objects.get(url=room_name)
            key = room_model.key
            if key not in creator.chat_keys:
                #print('creator', creator.first_name)
                creator.chat_keys.append(key)
                creator.save()
            if key not in second_person.chat_keys:
                second_person.chat_keys.append(key)
                second_person.save()
            return ChatModel.objects.get(url=room_name)
        
        
def verify_chat_member(request, room_name):
    model = ChatModel.objects.get(url=room_name)
    user = Account.objects.get(id=request.user.id)
    #print(model.key, user.chat_keys, user.first_name) 
    if model.key not in user.chat_keys:
        #print('FLASEEEEEE1')
        return False
    
    if user.id not in model.users:
        return False
    
    return True       
     
def chat_key_seeder(creator_id, second_id):
    prime = 67280421310721
    #prime = 1
    #print(creator_id, second_id, prime)
    seed = abs(hash(int(creator_id) * int(prime) - int(second_id)))
    random.seed(seed)
    key = random.randrange(1, seed)
    #print(seed, url)
    return key

def load_chat_log(request, room_name):
    user = Account.objects.get(id=request.user.id)#created_by
    user_name = user.first_name
    text_log = []
    lr_arr = []
    message_combined = []
    room_model = ChatModel.objects.get(url=room_name)
    room_log = room_model.messages
    for line in room_log:
        temp = []
        line = line.strip()
        line = line[12:-2]
        text_log.append(line + '\n\n')     
        temp.append(line + '\n\n')
        
        line_spl = line.split(':')
        #print(line_spl, user_name)
        if line_spl[0] == user_name:
            lr_arr.append('right')
            temp.append('right')
        else:
            lr_arr.append('left')
            temp.append('left')
        
        message_combined.append(temp)
    
    #print('pop1:',text_log.pop(0))
    #print('pop2:',lr_arr.pop(0))
    message_combined.pop(0)
    #print(text_log, lr_arr)
    #print(text_log)
    #print(lr_arr)
    
    
    return text_log, lr_arr, message_combined

def url_scrambler(id):
    hashed = urllib.parse.quote(chr(id))
    print(hashed)
    #hashed = abs(hash(str(id)))
    #print(hashed, id, 'hashed url')
    
    return hashed

def edit_chat_settings(request):
    pass

#debug
def clear_all_chats(request):
    for chat in ChatModel.objects.all():
        chat.delete()
        
    return redirect('hometemplate')      
        
def clear_user_keys(request):
    for account in Account.objects.all():
        account.chat_keys = []
        account.save()
        
    return redirect('hometemplate')     
#from chat/views import list_all_people
def list_all_people():
    all_people = Account.objects.all()
    return all_people


