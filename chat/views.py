# chat/views.py
from django.shortcuts import render, redirect
from authorize_main.models import Account
from Notifications.models import NotificationModel
from authorize_main.models import Account
from .models import ChatModel
import random
from django.http import HttpResponse

#from chat.views import chat_key_seeder, create_private_chat, notify_chat, url_scrambler

def index(request):
    user = Account.objects.get(id=request.user.id)
    return render(request, 'chat/index.html', {'user': user})

def room(request, room_name):
    user = Account.objects.get(id=request.user.id)#created_by
    user_name = user.first_name
    message_combined = ['']
    room_model = ChatModel.objects.filter(url=room_name)
    
    if len(room_model) == 0:
        #create new model
        ChatModel.objects.create(url=room_name, users=[user.id], messages=[''])
    #verify
    if verify_chat_member(request, room_name) == True:
        message_combined = load_chat_log(request, room_name)  
        
    
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'user': user,
            'message_combined': message_combined,
        })
    else:
        return HttpResponse('Account Denied')

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
            
            ChatModel.objects.create(users=[request.user.id, second_person_id], owner=creator.id, url=room_name, messages=[''], key=key)
            if key not in creator.chat_keys:
                #print('creator', creator.first_name)
                creator.chat_keys.append(key)
                creator.save()
            if key not in second_person.chat_keys:
                second_person.chat_keys.append(key)
                second_person.save()
            print(room_name)
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
    print(model.key, user.chat_keys, user.first_name) 
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
    message_combined = ['']
    room_model = ChatModel.objects.get(url=room_name)
    room_log = room_model.messages
    for line in room_log:
        line = line.strip()
        line = line[12:-2]
        text_log.append(line + '\n\n')     
        
        line_spl = line.split(':')
        #print(line_spl, user_name)
        if line_spl[0] == user_name:
            lr_arr.append('right')
        else:
            lr_arr.append('left')
        
        message_combined = zip(text_log, lr_arr)
    
    return message_combined


def url_scrambler(id):
    hashed = abs(hash(str(id)))
    print(hashed, id, 'a')
    
    return hashed

#debug
def clear_all_chats(request):
    for chat in ChatModel.objects.all():
        chat.delete()
        
    return redirect('index')      
        
def clear_user_keys(request):
    for account in Account.objects.all():
        account.chat_keys = []
        account.save()
        
    return redirect('index')     