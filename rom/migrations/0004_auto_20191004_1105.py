# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-10-04 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0003_class_sort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='rom/class/'),
        ),
    ]
