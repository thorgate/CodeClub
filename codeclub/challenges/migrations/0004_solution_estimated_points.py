# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import challenges.models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_auto_20151123_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='estimated_points',
            field=challenges.models.SolutionEstimateField(blank=True, null=True),
        ),
    ]
