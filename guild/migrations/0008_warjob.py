# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-24 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0006_auto_20191024_0725'),
        ('guild', '0007_auto_20191022_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('war', models.IntegerField(choices=[(0, 'WOE'), (1, 'WOC'), (2, 'ZONE')], db_index=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guild_war_jobs', related_query_name='guild_war_job', to='rom.CharacterBase')),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_war_jobs', related_query_name='member_war_job', to='guild.Guild')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rom.Job')),
            ],
        ),
    ]
