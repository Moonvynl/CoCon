# Generated by Django 5.0.6 on 2024-08-22 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_system', '0003_remove_chat_members_chat_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
