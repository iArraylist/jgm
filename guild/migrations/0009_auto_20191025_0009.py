# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-24 17:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0008_warjob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warjob',
            name='job',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rom.Job'),
        ),
        migrations.AlterField(
            model_name='warjob',
            name='war',
            field=models.IntegerField(choices=[(0, 'woe'), (1, 'woc'), (2, 'zone')], db_index=True),
        ),
    ]
