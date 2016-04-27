# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0011_challenge_golf'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='solution_size',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
