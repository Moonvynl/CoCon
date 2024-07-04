from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from user.models import CustomUser
from django.views.decorators.csrf import csrf_exempt


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'cocon/home.html')
        else:
            return render(request, 'user/login.html')


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
