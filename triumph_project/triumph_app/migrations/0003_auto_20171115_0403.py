# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('triumph_app', '0002_remove_challenge_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='level',
            field=models.PositiveIntegerField(default=1, verbose_name=b'\xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='sequence',
            field=models.CharField(max_length=255, verbose_name=b'\xd0\x92\xd1\x8b\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='coefficient',
            field=models.PositiveIntegerField(default=1, verbose_name=b'\xd0\x9c\xd0\xbd\xd0\xbe\xd0\xb6\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='theme_title',
            field=models.CharField(max_length=255, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x82\xd0\xb5\xd0\xbc\xd1\x8b'),
            preserve_default=True,
        ),
    ]
