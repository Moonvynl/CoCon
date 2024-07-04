# Generated by Django 4.1.13 on 2024-07-01 08:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat_system', '0002_alter_chat_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='members',
        ),
        migrations.AddField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
