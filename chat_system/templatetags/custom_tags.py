from django import template
from user.models import CustomUser
from django.http import HttpResponse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='remove_request_user')
def remove_request_user(queryset, request_user):
    user = queryset.members.exclude(id=request_user).first()
    html = f'''
    <li class="chat-item">
        <img src="{user.avatar.url}" alt="Avatar" class="chat-avatar">
        <div class="chat-details">
            <a href="/chat/{user.id}/">{user.username}</a>
            <p class="chat-last-message">user.last_message.content</p>
        </div>
    </li>
    '''
    return mark_safe(html)