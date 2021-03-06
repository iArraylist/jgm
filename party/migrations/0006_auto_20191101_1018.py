# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-01 10:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0005_party_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partymember',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='party_members', related_query_name='party_member', to='party.Party'),
        ),
    ]
