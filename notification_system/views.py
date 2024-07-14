from django.shortcuts import render
from django.views.generic import ListView, View
from user.models import FollowRequest
from django.shortcuts import redirect
from notification_system.models import Notification
from django.core.paginator import Paginator
from itertools import chain
from operator import attrgetter


class NotificationList(ListView):
    template_name = 'notification_system/notification_list.html'

    def get(self, request, *args, **kwargs):
        following_requests = FollowRequest.objects.filter(to_user=request.user)
        notifications = Notification.objects.filter(user=request.user)

        combined_list = list(chain(following_requests, notifications))

        paginator = Paginator(combined_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        prev_page_number = request.session.get('prev_page_number')

        if prev_page_number:
            prev_page_obj = paginator.get_page(prev_page_number)
            for obj in prev_page_obj:
                obj.is_seen = True
                obj.save()

        request.session['prev_page_number'] = page_number
    
        context = {
            'page_obj':page_obj,
        }
        
        return render(request, self.template_name, context=context)


class ActionFollowRequest(View):
    def post(self, request, *args, **kwargs):
        follow_request = FollowRequest.objects.get(id=kwargs['pk'])
        
        action = request.POST.get('action')
        if action == 'accept':
            if follow_request.to_user == request.user:
                follow_request.to_user.followers.add(follow_request.from_user)
                follow_request.from_user.following.add(follow_request.to_user)
                follow_request.delete()
            return redirect('notification_system:notifications')
        elif action == 'reject':
            if follow_request.to_user == request.user:
                follow_request.delete()
            return redirect('notification_system:notifications')

