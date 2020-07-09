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

def main_chat_room(request): #Beta chat room to see avaliable chats
    user = Account.objects.get(id=request.user.id)
    chats = []
    for key in user.chat_keys:
        check = ChatModel.objects.filter(key=key)
        
        for x in check:
            chats.append(x)
    
    return render(request, 'chat/index.html', {'user': user, 'friends':user.friends, 'chats':chats})

def change_chat_room(request, chat_url):
    return redirect(f'/chat/{chat_url}')
    
def room(request, room_name): #load chat log, verify users
    other_guy = ''
    user = Account.objects.get(id=request.user.id)#created_by
    user_name = user.first_name
    message_combined = ['']
    room_model = ChatModel.objects.filter(url=room_name)
    
    #verify
    if verify_chat_member(request, room_name) == True:
        text_log, lr_arr, message_combined = load_chat_log(request, room_name)
        room_model = ChatModel.objects.get(url=room_name)
        
        id_arr = room_model.users

        for x in id_arr:
            person = Account.objects.get(id=x)
            
            if person.id != user.id:
                other_guy = person
            
        
        img_src = other_guy.profile_pic.url
        user_img = user.profile_pic.url
        
        chat_keys = user.chat_keys
        chat_rooms = []
        
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
           chat_times[chat_collection[0].last_updated] = None

        for chat_collection in chat_rooms:
            time_key_lst.append(chat_collection[0].last_updated)
            
            if chat_times[chat_collection[0].last_updated] is None: 
                chat_times[chat_collection[0].last_updated] = [chat_collection]
            elif chat_times[chat_collection[0].last_updated] is not None:
                chat_times[chat_collection[0].last_updated].append(chat_collection)
            
        time_key_lst = sorted(time_key_lst)

        chat_room_organized = []
        
        for chat in time_key_lst:
            
            if len(chat_times[chat]) > 1:
                for i in chat_times[chat]:
                    if i not in chat_room_organized:
                        chat_room_organized.append(i)
            else:
                    if chat_times[chat][0] not in chat_room_organized:
                        chat_room_organized.append(chat_times[chat][0])
    
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


def create_private_chat(request, room_name, second_person_id=None, post_id=1, owner_id= None): #creates chat with parameters
    if not owner_id:
        
        creator = Account.objects.get(id=request.user.id)
    else:
        creator = Account.objects.get(id=owner_id) 
    
    room_model = ChatModel.objects.filter(url=room_name)
    if post_id != 1:
        post_name = PostModel.objects.get(id= post_id).title_of_post
        
    if second_person_id:
        second_person = Account.objects.get(id=second_person_id)
        key = chat_key_seeder(creator.id, second_person_id, post_id)
    
        if len(room_model) == 0:
             
            if post_id != 1:
                ChatModel.objects.create(users=[creator.id, second_person_id], owner=creator.id, url=room_name, chat_name=creator.first_name + "'s Chat for post: " + post_name, messages=[''], key=key)
            else:
               ChatModel.objects.create(users=[creator.id, second_person_id], owner=creator.id, url=room_name, chat_name=creator.first_name + "'s and " + second_person.first_name + "'s chat", messages=[''], key=key) 
            room_model = ChatModel.objects.get(url=room_name)
            
            if key not in creator.chat_keys:
                
                creator.chat_keys.append(key)
                creator.save()
            if key not in second_person.chat_keys:
                second_person.chat_keys.append(key)
                second_person.save()
           
            notify_chat(request, creator.id)
            return ChatModel.objects.get(url=room_name)
            
        else: 
            room_model = ChatModel.objects.get(url=room_name)
            key = room_model.key
            if key not in creator.chat_keys:
                
                creator.chat_keys.append(key)
                creator.save()
            if key not in second_person.chat_keys:
                second_person.chat_keys.append(key)
                second_person.save()
            return ChatModel.objects.get(url=room_name)
        
        
def verify_chat_member(request, room_name): #verifys user and chat keys
    model = ChatModel.objects.get(url=room_name)
    user = Account.objects.get(id=request.user.id)
    
    if model.key not in user.chat_keys:
        
        return False
    
    if user.id not in model.users:
        return False
    
    return True       
     
def chat_key_seeder(creator_id, second_id, post_id=None): # make unique keys(passwords) for chat 
    prime = 67280421310721
   
    seed = abs(hash(int(creator_id) * int(prime) - int(second_id))) * post_id
    random.seed(seed)
    key = random.randrange(1, seed)
    
    return key

def load_chat_log(request, room_name): #loads chat log
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
       
        if line_spl[0] == user_name:
            lr_arr.append('right')
            temp.append('right')
        else:
            lr_arr.append('left')
            temp.append('left')
        
        message_combined.append(temp)
    
    message_combined.pop(0)
    
    return text_log, lr_arr, message_combined

def url_scrambler(id): # encodes chat room URL to prevent hacking
    hashed = urllib.parse.quote(chr(id))
    
    hashstr = ''
    hashed = hashed.split('%')
    
    for letter in hashed:
        hashstr += letter
    return hashstr

def edit_chat_settings(request):
    pass

def route_to_chat(request, second_id):
    pass
    
#from chat/views import list_all_people
def list_all_people():
    all_people = Account.objects.all()
    return all_people

def notify_chat(request, second):
    pass

def friend_chat(request, other_id):
    user_one = request.user.id
    user_two = other_id
    
    if Account.objects.get(id=user_one).id in Account.objects.get(id=user_two).friends and Account.objects.get(id=user_two).id in Account.objects.get(id=user_one).friends:
         
        higher_id = max(user_one, user_two)
        lower_id = min(user_one, user_two) 

        url = url_scrambler(higher_id) + "EEE" + url_scrambler(lower_id)

        create_private_chat(request, url, other_id)
        
        return room(request, url)
 
    else:
        return HttpResponse(f"You are not friends with this person!")
    
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