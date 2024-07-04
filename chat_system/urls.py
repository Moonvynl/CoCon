from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('chatlist', chat_list, name='chat_list'),
    path('chat/<int:pk>/', chat_create_if_not_exists, name='chat'),
    path('chat', chat_base, name='chat'),
]

app_name = 'chat_system'