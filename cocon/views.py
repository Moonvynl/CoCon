from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from user.models import CustomUser
from notification_system.models import Notification
from user.models import FollowRequest
from post_system.models import *
from django.contrib.auth.mixins import LoginRequiredMixin



class LeftMenuView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            unread_messages = 0
            notifications = Notification.objects.filter(user=request.user, is_seen=False)
            followrequests = FollowRequest.objects.filter(to_user=request.user)
            for notification in notifications:
                unread_messages += 1
            for followrequest in followrequests:
                unread_messages += 1

            context = {
                'unread_messages': unread_messages
            }
        return render(request, 'cocon/left_menu.html', context=context)


def search_view(request):
    return render(request, 'cocon/search/search.html')

def search_results(request):
    query = request.GET.get('search', '')

    all_users = CustomUser.objects.all()
    if query:
        users = all_users.filter(username__icontains=query)
    else:
        users = []

    context = {
        'users': users[:5]
    }

    return render(request, 'cocon/search/search_results.html', context)


class InterestingsView(ListView):
    model = Post
    template_name = 'cocon/interestings.html'
    
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__profile_is_private=False)


class NewsFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'cocon/news_feed.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        super().get(request)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'cocon/post.html', context=self.get_context_data())
        
        return render(request, self.template_name, self.get_context_data())

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__in=self.request.user.following.all())
