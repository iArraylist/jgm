# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-25 09:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0006_auto_20191024_0725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['sort']},
        ),
    ]
