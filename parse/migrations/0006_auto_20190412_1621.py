# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-12 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0005_loads_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loads',
            name='created_at',
        ),
        migrations.AddField(
            model_name='loads',
            name='last_found',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
