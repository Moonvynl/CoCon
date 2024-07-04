from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View
from .models import CustomUser
from post_system.models import Post
from django.contrib.auth.decorators import login_required
from .mixins import *
from django.utils.decorators import method_decorator


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
        return render(request, self.template_name, {'user':user,
                                            'following': user_following_count,
                                            'followers': user_follower_count,
                                            'user_posts_count': user_posts_count,
                                            'user_posts': user_posts,
                                            })

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
