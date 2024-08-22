from django import template
from django.utils.safestring import mark_safe
from chat_system.models import Chat

register = template.Library()

@register.filter(name='remove_request_user')
def remove_request_user(queryset, request_user):
    user = queryset.members.exclude(id=request_user).first()
    chat = Chat.objects.filter(members__id=user.id).filter(members__id=request_user)
    last_message = chat[0].messages.all().last()
    if chat[0].messages.filter(is_seen=False).exclude(sender=request_user).exists():
        html = f'''
        <a href="/create-chat/{user.id}/">
        <li class="chat-item unread-chat">
            <img src="{user.avatar.url}" alt="Avatar" class="chat-avatar">
            <div class="chat-details">
                <a href="/create-chat/{user.id}/">{user.username}</a>
                <p class="chat-last-message">{str(last_message)[:25]+'...' if len(str(last_message)) >= 25 else last_message or '' }</p>
            </div>
        </li>
        </a>
        '''
    else:
        html = f'''
        <a href="/create-chat/{user.id}/">
        <li class="chat-item">
            <img src="{user.avatar.url}" alt="Avatar" class="chat-avatar">
            <div class="chat-details">
                <a href="/create-chat/{user.id}/">{user.username}</a>
                <p class="chat-last-message">{str(last_message)[:25]+'...' if len(str(last_message)) >= 25 else last_message or '' }</p>
            </div>
        </li>
        </a>
        '''
    return mark_safe(html)