from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, View, TemplateView, DeleteView
from .models import *
from .forms import PostCreateForm
from .mixins import RedirectToPreviousMixin


class CreatePostView(RedirectToPreviousMixin ,CreateView):
    def post(self, request, *args, **kwargs):
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            Post.objects.create(
                user=request.user,
                content=form.cleaned_data.get('content'),
                description=form.cleaned_data.get('description')
            ).save()
            return redirect('user:profile', pk = request.user.id)