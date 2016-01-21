# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0006_auto_20151209_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='requirements',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
