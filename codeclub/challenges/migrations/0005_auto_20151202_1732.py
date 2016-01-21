# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_solution_estimated_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Submitted'), (10, 'In progress'), (15, 'Got timeout'), (20, 'Wrong'), (30, 'Correct')]),
        ),
    ]
