# chat/views.py
from django.shortcuts import render, redirect
from authorize_main.models import Account
from Notifications.models import NotificationModel
from authorize_main.models import Account
from .models import ChatModel
from posts_app.models import PostModel
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

def change_chat_room(request, chat_url):
    return redirect(f'/chat/{chat_url}')
    
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
            #print(person.id)
            #print(user.id)
            if person.id != user.id:
                other_guy = person
            
        
        img_src = other_guy.profile_pic.url
        user_img = user.profile_pic.url
        
        chat_keys = user.chat_keys
        chat_rooms = []
        print(user.first_name, other_guy.first_name)
        for room_key in chat_keys:
            chat = ChatModel.objects.filter(key = room_key)
            if len(chat) > 0:
                chat = ChatModel.objects.get(key = room_key)
                for ids in chat.users:
                    if ids != request.user.id:
                        other_user = Account.objects.get(id = ids)
                        chat_img = other_user.profile_pic
                        chat_name = other_user.first_name + ' ' + other_user.last_name
                        chat_rooms.append([chat, chat.url, chat_img, chat_name])

        chat_times = {}
        time_key_lst = []

        for chat_collection in chat_rooms:
            time_key_lst.append(chat_collection[0].last_updated)
            chat_times[chat_collection[0].last_updated] = chat_collection
            
        time_key_lst = sorted(time_key_lst)
        chat_room_organized = []
        
        for chat in time_key_lst:
            chat_room_organized.append(chat_times[chat])

        chat_room_organized.reverse()
        
        return render(request, 'chat/room.html', {
            "room_name": room_name,
            "room_title": room_model.chat_name,
            "message_combined":message_combined,
            "img_src":img_src,
            "user_img":user_img,
            "friends":list_all_people(),
            "chat_rooms":chat_room_organized,
        })

    #notification.save()

def create_private_chat(request, room_name, second_person_id=None, post_id=None, owner_id= None):
    if not owner_id:
        
        creator = Account.objects.get(id=request.user.id)
    else:
        creator = Account.objects.get(id=owner_id) 
    
    room_model = ChatModel.objects.filter(url=room_name)
    post_name = PostModel.objects.get(id= post_id).title_of_post
    if second_person_id:
        second_person = Account.objects.get(id=second_person_id)
        key = chat_key_seeder(creator.id, second_person_id, post_id)
        #print(room_name, request.user.id, second_person_id, key)
        if len(room_model) == 0:
             #print(creator.chat_keys, second_person.chat_keys)
            ChatModel.objects.create(users=[creator.id, second_person_id], owner=creator.id, url=room_name, chat_name=creator.first_name + "'s Chat for post: " + post_name, messages=[''], key=key)
            room_model = ChatModel.objects.get(url=room_name)
            #print(room_model.users)
            if key not in creator.chat_keys:
                #print('creator', creator.first_name)
                creator.chat_keys.append(key)
                creator.save()
            if key not in second_person.chat_keys:
                second_person.chat_keys.append(key)
                second_person.save()
            #print(room_name)
            notify_chat(request, creator.id)
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
     
def chat_key_seeder(creator_id, second_id, post_id=None):
    prime = 67280421310721
    #prime = 1
    #print(creator_id, second_id, prime)
    seed = abs(hash(int(creator_id) * int(prime) - int(second_id))) * post_id
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
    #print(hashed)
    #hashed = abs(hash(str(id)))
    #print(hashed, id, 'hashed url')
    hashstr = ''
    hashed = hashed.split('%')
    
    for letter in hashed:
        hashstr += letter
    return hashstr

def edit_chat_settings(request):
    pass

def route_to_chat(request, second_id):
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

def notify_chat(request, second):
    pass
