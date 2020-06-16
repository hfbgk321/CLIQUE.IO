# chat/views.py
from django.shortcuts import render
from authorize_main.models import Account
from Notifications.models import NotificationModel
from authorize_main.models import Account
from .models import ChatModel

def index(request):
    user = Account.objects.get(id=request.user.id)
    return render(request, 'chat/index.html', {'user': user})

def room(request, room_name):
    user = Account.objects.get(id=request.user.id)#created_by
    text_log = ""
    room_model = ChatModel.objects.filter(id=int(room_name))
    
    if len(room_model) == 0:
        ChatModel.objects.create(id=int(room_name), users=[user.id], messages=[])
    else:
        room_model = ChatModel.objects.get(id=int(room_name))
        room_log = room_model.messages
        text_log = ''

        for line in room_log:
            text_log = text_log + '\n' + line
    
    #ext_log = "hi\nhey\nnew"
     
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user': user,
        'text_log': text_log,
    })

def start_chat(request, user_id, applicant_id):
    notification = NotificationModel.objects.create(account=request.user,notified_message =f'{Account.objects.get(id=user_id).first_name} {Account.objects.get(id=user_id).last_name} wants to chat!')
    notification.save()
    
    return redirect('')
    