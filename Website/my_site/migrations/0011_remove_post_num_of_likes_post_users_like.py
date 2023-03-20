# Generated by Django 4.1.7 on 2023-03-17 11:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_site', '0010_remove_post_likes_post_num_of_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='num_of_likes',
        ),
        migrations.AddField(
            model_name='post',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='post_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]