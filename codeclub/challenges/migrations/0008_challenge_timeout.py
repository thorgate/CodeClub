# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0007_challenge_requirements'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='timeout',
            field=models.FloatField(default=10),
        ),
    ]
