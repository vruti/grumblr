# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_auto_20150925_0139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile_info',
            name='age',
        ),
        migrations.AddField(
            model_name='profile_info',
            name='dob',
            field=models.DateTimeField(verbose_name='date of birth', default=datetime.date.today),
        ),
    ]
