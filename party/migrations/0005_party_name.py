# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-25 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0004_auto_20191025_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
