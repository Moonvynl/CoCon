from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse

def createchat(request, pk):
    user1 = get_object_or_404(CustomUser, pk=request.user.pk)
    user2 = get_object_or_404(CustomUser, pk=pk)
    chat = Chat.objects.filter(members__id=user1.id).filter(members__id=user2.id)
    if chat.exists():
        return redirect('chat_system:chat-detail', pk=chat[0].pk)
    else:
        chat = Chat.objects.create()
        chat.members.add(user1, user2)
        return redirect('chat_system:chat-detail', pk=chat.pk)

def chat_detail(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    receiver = chat.members.all().exclude(id=request.user.id)[0]
    messages = chat.messages.all()
    return render(request, 'chat_system/chat.html', {'chat': chat, 'messages': messages, 'receiver':receiver})

def chat_list(request):
    if request.method == 'GET':
        chats = Chat.objects.filter(members__id=request.user.id)
        return render(request, 'chat_system/chat_list.html', {'chats': chats})

def chat_base(request):
    if request.method == 'GET':
        return render(request, 'chat_system/chat_base.html')


class SendMessageView(View):
    def post(self, request, *args, **kwargs):
        chat_id = kwargs.get('pk')
        chat = Chat.objects.filter(pk=chat_id)
        content = request.POST.get('content')
        sender = request.user
        message = Message.objects.create(chat=chat[0],
                            sender=sender,
                            content=content)
        message.save()
        return redirect('chat_system:chat-detail', pk=chat_id)