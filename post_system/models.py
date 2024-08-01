from django.db import models
from user.models import CustomUser


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    hashtags = models.ManyToManyField('Hashtag', blank=True)

    content = models.FileField(upload_to='posts/')
    description = models.TextField(max_length=2200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')

    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    content = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.user


class Hashtag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    post_count = models.IntegerField(default=0)

    def count_posts(self):
        self.post_count = Post.objects.filter(content__icontains=self.title).count()
        self.save()

    def __str__(self):
        return self.title

