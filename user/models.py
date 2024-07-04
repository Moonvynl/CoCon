from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, default='/default_avatar.png')
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField('self', related_name='user_followers', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='user_following', symmetrical=False, blank=True)

    def __str__(self):
        return self.username