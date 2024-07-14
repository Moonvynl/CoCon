from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View
from .models import *
from post_system.models import Post
from django.contrib.auth.decorators import login_required
from .mixins import *
from django.utils.decorators import method_decorator
from notification_system.models import Notification
from django.utils import timezone



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "user/register.html"
    success_url = reverse_lazy("cocon:home")
    def form_valid(self, form):
        user = form.save()
    
        if user:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            if user.is_authenticated:
                return HttpResponseRedirect(self.success_url)
            else:
                return redirect("user:login")

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserProfileView(View, UserIsOwnerMixin):
    template_name = "user/user_profile.html"

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['pk'])
        user_follower_count = user.followers.count()
        user_following_count = user.following.count()
        user_posts_count = Post.objects.filter(user=user).count()
        user_posts = Post.objects.filter(user=user)

        user_profile_is_private = user.profile_is_private
        user_is_followed = user.followers.filter(id=request.user.id).exists() or user.id == request.user.id
        follow_request_exists = FollowRequest.objects.filter(from_user=request.user, to_user=user)

        context = {
            'user':user,
            'following': user_following_count,
            'followers': user_follower_count,
            'user_posts_count': user_posts_count,
            'user_posts': user_posts,
            'user_profile_is_private': user_profile_is_private,
            'user_is_followed': user_is_followed,
            'follow_request': follow_request_exists,
        }

        return render(request, self.template_name, context=context)


@method_decorator(login_required, name='dispatch')
class UpdateUserInfo(View, UserIsOwnerMixin):
    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        
        if CustomUser.objects.filter(username=request.POST.get('username')).exclude(id=request.user.id).exists():
            messages.error(request, "Username already exists")
            return render(request, "user/change_user_info.html", {'form':form})
        else:
            if form.is_valid():
                form.save()
                return redirect('user:profile', pk=request.user.id)
    
    def get(self, request, *args, **kwargs):
        form = UserUpdateForm(instance=request.user)
        return render(request, "user/change_user_info.html", {'form':form})


class FollowUser(View):
    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['pk'])
        request_user = request.user
        user_is_followed = user.followers.filter(id=request.user.id).exists()
        if user_is_followed:
            user.followers.remove(request.user)
            request_user.following.remove(user)
        elif not user_is_followed:
            if user.profile_is_private:
                FollowRequest.objects.create(from_user=request.user, to_user=user)
            else:
                Notification.objects.create(user = user,
                                            message= f'{request_user.username} followed {user.username} ',
                                            html = (
        f'        <img src="{request_user.avatar.url}" alt="Profile Picture" class="profile-picture">'
        f'        <div class="notification-message">'
        f'            <a href="/profile/{request_user.id}/">{request_user.username}</a> підписався(-лась) на вас'
        f'        </div>'
    )
)
                user.followers.add(request.user)
                request_user.following.add(user)
        return redirect('user:profile', pk=user.id)

