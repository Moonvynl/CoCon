from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404


def chat_create_if_not_exists(request, pk):
    if request.method == 'GET':
        current_user = request.user
        chat = Chat.objects.filter(members__id=pk).filter(members__id=request.user.id)
        if chat.exists():
            receiver = chat[0].members.all().exclude(id=current_user.id)[0]
            return render(request, 'chat_system/chat.html', {'chat': chat, 'receiver': receiver})
        else:
            user1 = CustomUser.objects.get(id=request.user.id)
            user2 = CustomUser.objects.get(id=pk)
            new_chat = Chat.objects.create()
            new_chat.members.add(user1, user2)
            receiver = chat[0].members.all().exclude(id=current_user.id)[0]
            return render(request, 'chat_system/chat.html', {'chat': new_chat, 'receiver': receiver})
    else:
        return render(request, 'chat_system/error.html', {'error': 'Invalid request method'})


def chat_list(request):
    if request.method == 'GET':
        chats = Chat.objects.filter(members__id=request.user.id)
        return render(request, 'chat_system/chat_list.html', {'chats': chats})

def chat_base(request):
    if request.method == 'GET':
        return render(request, 'chat_system/chat_base.html')