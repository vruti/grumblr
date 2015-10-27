# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0006_auto_20151008_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('photo', models.ImageField(default='/static/images/no-image.png', upload_to='images')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('dob', models.DateTimeField(null=True, blank=True)),
                ('bio', models.CharField(blank=True, max_length=430)),
                ('following', models.ManyToManyField(related_name='followedUsers', to='grumblr.ProfileInfo')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile_info',
            name='following',
        ),
        migrations.RemoveField(
            model_name='profile_info',
            name='user',
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name='user_profile', to='grumblr.ProfileInfo'),
        ),
        migrations.DeleteModel(
            name='Profile_Info',
        ),
    ]
