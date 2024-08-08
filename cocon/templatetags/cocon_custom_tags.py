from django import template
from post_system.models import Post, Like


register = template.Library()

@register.filter(name='likes_count')
def likes_count(model):
    id = model.id
    post = Post.objects.get(id=id)
    likes_count = Like.objects.filter(post=post).count()
    return likes_count

@register.filter(name='is_liked')
def is_liked(model,user):
    id = model.id
    post = Post.objects.get(id=id)
    is_liked = Like.objects.filter(post=post, user=user).exists()
    return is_liked