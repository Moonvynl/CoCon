# Generated by Django 5.0.6 on 2024-07-30 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_system', '0004_remove_post_hashtags_post_hashtags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='hashtags',
        ),
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='post_system.hashtag'),
        ),
    ]
