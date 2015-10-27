# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0007_auto_20151008_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileinfo',
            name='photo',
            field=models.ImageField(upload_to='/static/images', default='/static/images/no-image.png'),
        ),
    ]
