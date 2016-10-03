# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0011_auto_20160427_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='output',
            field=models.TextField(blank=True),
        ),
    ]
