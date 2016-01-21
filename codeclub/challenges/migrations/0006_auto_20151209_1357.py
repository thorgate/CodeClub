# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_auto_20151202_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='event',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
