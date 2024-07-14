from django.db import models
from django.conf import settings


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    html = models.TextField(default=None, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['-date', 'is_seen']