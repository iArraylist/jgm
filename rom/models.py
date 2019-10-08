from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Job(models.Model):
    name = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='rom/class/', blank=True, null=True, default=None)
    sort = models.IntegerField(default=0)


class CharacterBase(models.Model):
    member = models.ForeignKey('auth.User')
    ign = models.CharField(max_length=255)
    base_level = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(120), MinValueValidator(1)])
    contribution = models.PositiveIntegerField(default=0)
    gold_medal = models.PositiveIntegerField(default=0)


class CharacterJob(models.Model):
    base = models.ForeignKey('rom.CharacterBase', db_index=True)
    job = models.ForeignKey('rom.Job', db_index=True)
    image = models.ImageField(upload_to='rom/character/', blank=True, null=True, default=None)


