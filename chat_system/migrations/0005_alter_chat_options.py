# Generated by Django 5.0.6 on 2024-08-22 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_system', '0004_message_is_seen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['-messages__is_seen', '-id']},
        ),
    ]
