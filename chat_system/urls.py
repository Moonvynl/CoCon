from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('chatlist/', chat_list, name='chat_list'),
    path('create-chat/<int:pk>/', createchat, name='create-chat'),
    path('chat/<int:pk>/', chat_detail, name='chat-detail'),
    path('chat/', chat_base, name='chat'),
    path('chat/<int:pk>/send-message/', SendMessageView.as_view(), name='send-message'),
]

app_name = 'chat_system'