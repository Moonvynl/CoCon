from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html' , extra_context={'next': reverse_lazy('cocon:home')}), name='login'),
    path('register/', RegisterView.as_view(template_name='user/register.html'), name='register'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('user:login')), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('update-user-info/<int:pk>/', UpdateUserInfo.as_view(), name='update-user-info'),
    path('follow/<int:pk>/', FollowUser.as_view(), name='follow'),
]

app_name = 'user'