# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0008_auto_20151022_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='profileinfo',
            name='photo',
            field=models.ImageField(default='/static/images/no-image.png', upload_to='/media/images'),
        ),
    ]
