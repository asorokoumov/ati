# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-13 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0009_auto_20190426_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stopper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_stopped', models.BooleanField(default=False)),
            ],
        ),
    ]
