# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0012_solution_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='network_allowed',
            field=models.BooleanField(default=False),
        ),
    ]
