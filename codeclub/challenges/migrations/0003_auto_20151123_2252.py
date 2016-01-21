# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_auto_20151123_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='answer',
        ),
        migrations.AddField(
            model_name='challenge',
            name='tester',
            field=models.FileField(default='', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solution',
            name='solution',
            field=models.FileField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
