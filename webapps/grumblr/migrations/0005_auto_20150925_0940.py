# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_remove_profile_info_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_info',
            name='dob',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
