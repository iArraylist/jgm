# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-22 08:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0004_guildmember_line_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guildmember',
            name='line_contact',
        ),
    ]
