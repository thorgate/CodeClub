# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('public', models.BooleanField(default=True)),
                ('order', models.IntegerField(help_text='In ascending order')),
                ('author', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
    ]
