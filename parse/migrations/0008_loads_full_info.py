# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0007_parser'),
    ]

    operations = [
        migrations.AddField(
            model_name='loads',
            name='full_info',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
