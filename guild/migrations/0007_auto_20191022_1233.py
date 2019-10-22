# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-22 12:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0006_waitingapprove'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitingapprove',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waiting', related_query_name='waiting', to='rom.CharacterBase'),
        ),
        migrations.AlterField(
            model_name='waitingapprove',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waiting_list', related_query_name='waiting_list', to='guild.Guild'),
        ),
    ]
