# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20150925_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_info',
            name='bio',
            field=models.CharField(max_length=430, blank=True),
        ),
        migrations.AddField(
            model_name='profile_info',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='profile_info',
            name='following',
            field=models.ManyToManyField(to='grumblr.Profile_Info', related_name='followedUsers'),
        ),
        migrations.AddField(
            model_name='profile_info',
            name='photo',
            field=models.ImageField(upload_to='images', default='/static/images/no-image.png'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to='grumblr.Profile_Info', related_name='user_profile'),
        ),
        migrations.AlterField(
            model_name='profile_info',
            name='dob',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
