# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0010_auto_20160218_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='golf',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solution',
            name='solution_size',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
