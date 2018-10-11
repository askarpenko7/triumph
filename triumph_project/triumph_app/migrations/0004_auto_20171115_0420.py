# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('triumph_app', '0003_auto_20171115_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='sequence',
            field=models.CharField(max_length=999, verbose_name=b'\xd0\x92\xd1\x8b\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5'),
            preserve_default=True,
        ),
    ]
