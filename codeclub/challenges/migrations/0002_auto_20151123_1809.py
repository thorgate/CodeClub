# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solution',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='solution',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(10, 'In progress'), (20, 'Wrong'), (30, 'Correct')], default=10),
        ),
    ]
