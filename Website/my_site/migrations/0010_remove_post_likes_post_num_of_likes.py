# Generated by Django 4.1.7 on 2023-03-15 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0009_remove_post_num_of_likes_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='num_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]