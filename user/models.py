from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, default='/default_avatar.png')
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField('self', related_name='user_followers', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='user_following', symmetrical=False, blank=True)
    profile_is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class FollowRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user} хоче слідкувати за {self.to_user}"