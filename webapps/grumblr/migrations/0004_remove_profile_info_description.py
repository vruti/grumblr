# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0003_auto_20150925_0212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile_info',
            name='description',
        ),
    ]
