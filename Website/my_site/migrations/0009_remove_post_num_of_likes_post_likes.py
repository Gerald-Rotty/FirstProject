# Generated by Django 4.1.7 on 2023-03-15 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_site', '0008_remove_post_likes_post_num_of_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='num_of_likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='post_like', to=settings.AUTH_USER_MODEL),
        ),
    ]