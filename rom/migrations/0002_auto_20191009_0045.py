# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-08 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='characterbase',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='characterbase',
            name='status',
            field=models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], db_index=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='characterbase',
            name='update_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='characterjob',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='characterjob',
            name='status',
            field=models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], db_index=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='characterbase',
            name='contribution',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='characterbase',
            name='gold_medal',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='characterbase',
            name='ign',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='sort',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
