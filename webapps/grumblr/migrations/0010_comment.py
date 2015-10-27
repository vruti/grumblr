# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0009_auto_20151023_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('comment', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(to='grumblr.Post', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment')),
                ('user', models.ForeignKey(to='grumblr.ProfileInfo')),
            ],
        ),
    ]
