from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, View, TemplateView, DeleteView
from .models import *
from .forms import PostCreateForm
from .mixins import RedirectToPreviousMixin
from django.http import JsonResponse
from django.core.serializers import serialize
from notification_system.models import Notification


class CreatePostView(RedirectToPreviousMixin ,CreateView):
    def post(self, request, *args, **kwargs):
        form = PostCreateForm(data=request.POST, files=request.FILES)
        hashtag_list = []
        if request.POST.get('hashtags'):
            for hashtag in request.POST.get('hashtags').split():
                hashtagg = Hashtag.objects.get_or_create(title=hashtag)
                hashtag_list.append(hashtagg[0])
        else:
            hashtag_list = None

        if form.is_valid():
            post = Post.objects.create(
                user=request.user,
                content=form.cleaned_data.get('content'),
                description=form.cleaned_data.get('description'),
            )
            post.save()
            if hashtag_list:
                for i in hashtag_list:
                    post.hashtags.add(i)
            return redirect('user:profile', pk = request.user.id)
        else:
            return HttpResponse('Invalid form')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_system/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        context['likes'] = Like.objects.filter(post=self.get_object()).count()
        context['is_liked'] = Like.objects.filter(post=self.get_object(), user=self.request.user).exists()
        return context


def get_model_data(request, pk):
    try:
        instance = Post.objects.get(pk=pk)
        queryset = Comment.objects.filter(post=instance)
        comments = []
        hashtags = []
        for comment in queryset:
            comments.append({
                'id': comment.id,
                'post': comment.post_id,
                'username': comment.user.username,
                'user_avatar': comment.user.avatar.url,
                'content': comment.content,
                'created_at': comment.created_at,
            })
        if instance.hashtags.all():
            for hashtag in instance.hashtags.all():
                hashtags.append({
                    'id': hashtag.id,
                    'title': hashtag.title
                })
        data = {
            'id': instance.id,
            'user': instance.user.username,
            'user_id': instance.user.id,
            'user_avatar': instance.user.avatar.url,
            'content': instance.content.url,
            'description': instance.description,
            'created_at': instance.created_at,
            'likes_count': Like.objects.filter(post=instance).count(),
            'is_liked': Like.objects.filter(post=instance, user=request.user).exists(),

        }
        data['hashtags'] = hashtags
        data['comments'] = comments
        return JsonResponse(data)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Model not found'}, status=404)


def like_post(request):
    if request.method == 'POST':
        id = request.POST.get('postId')
        user_id = request.POST.get('userId')
        post = Post.objects.get(id=id)
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.filter(post=post, user=request.user).delete()
        else:
            Like.objects.create(post=post, user=request.user)
            if request.user.id != post.user.id:
                Notification.objects.create(user = CustomUser.objects.get(id = user_id),
                                    message= f'{request.user.username} liked post {post.id}',
                                    html = (
                f'        <img src="{request.user.avatar.url}" alt="Profile Picture" class="profile-picture">'
                f'        <div class="notification-message">'
                f'            <a href="/profile/{request.user.id}/">{request.user.username}</a> вподобав ваш пост'
                f'            <a><img class="post-action-img" src="{post.content.url}"></a>'
                f'        </div>'
                ))
        
        data = {
            'likes_count': Like.objects.filter(post=post).count(),
            'is_liked': Like.objects.filter(post=post, user=request.user).exists()
        }
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)
    
    return JsonResponse({'error': 'Invalid request'}) 

def comment_post(request):
    if request.method == 'POST':
        request_user = request.user
        post_id = request.POST.get('postIdCom')
        content = request.POST.get('com-content')
        user_id = request.POST.get('userIdCom')
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post, user=request_user, content=content)
        if request_user.id != post.user.id:
            Notification.objects.create(user = CustomUser.objects.get(id = user_id),
                                                message= f'{request_user.username} commented post {post_id}',
                                                html = (
            f'        <img src="{request_user.avatar.url}" alt="Profile Picture" class="profile-picture">'
            f'        <div class="notification-message">'
            f'            <a href="/profile/{request_user.id}/">{request_user.username}</a> коментував ваш пост: {content}'
            f'            <a><img class="post-action-img" src="{post.content.url}"></a>'
            f'        </div>'
            ))
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)


class HashtagPosts(ListView):
    model = Post
    template_name = 'post_system/hashtag_posts.html'
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        hashtag = Hashtag.objects.get(title=kwargs['pk'])
        posts = Post.objects.filter(hashtags=hashtag)
        context = {
            'posts': posts,
            'hashtag':hashtag,
        }
        return render(request, self.template_name, context)