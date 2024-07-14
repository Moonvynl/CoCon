from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('notifications/', NotificationList.as_view(), name='notifications'),
    path('notifications/following-request/<int:pk>/action', ActionFollowRequest.as_view(), name='action-follow-request'),

]

app_name = 'notification_system'