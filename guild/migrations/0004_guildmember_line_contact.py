# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-21 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0003_auto_20191021_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='guildmember',
            name='line_contact',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
