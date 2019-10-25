# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-25 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_auto_20191025_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partymember',
            name='war_job',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='party_m_list', related_query_name='party_m', to='guild.WarJob'),
        ),
    ]
