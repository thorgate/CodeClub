# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tg_utils.files


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0009_add_author_to_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='requirements',
            field=models.FileField(blank=True, upload_to=tg_utils.files.random_path, null=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='tester',
            field=models.FileField(upload_to=tg_utils.files.random_path),
        ),
        migrations.AlterField(
            model_name='solution',
            name='solution',
            field=models.FileField(upload_to=tg_utils.files.random_path),
        ),
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Submitted'), (10, 'In progress'), (15, 'Timed out'), (20, 'Wrong'), (30, 'Correct')]),
        ),
    ]
