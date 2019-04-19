# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0008_loads_full_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='loads',
            name='parser',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='parse.Parser'),
            preserve_default=False,
        ),
    ]
