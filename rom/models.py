# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from guild.models import GuildMember
from django.conf import settings


CHARACTER_STATUS = (
    (0, 'Inactive'),
    (1, 'Active'),
)


class Job(models.Model):
    name = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='rom/class/', blank=True, null=True, default=None)
    sort = models.IntegerField(default=0, db_index=True)


class CharacterBase(models.Model):
    member = models.ForeignKey('auth.User', db_index=True)
    ign = models.CharField(max_length=255, db_index=True)
    base_level = models.PositiveSmallIntegerField(default=1, db_index=True)
    contribution = models.PositiveIntegerField(default=0, db_index=True)
    gold_medal = models.PositiveIntegerField(default=0, db_index=True)
    status = models.IntegerField(choices=CHARACTER_STATUS, db_index=True, default=1)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def check_job(self, job_id):
        if CharacterJob.objects.filter(base=self, job_id=job_id).exists():
            return True
        return False

    def get_jobs(self):
        return CharacterJob.objects.filter(base=self)

    def get_guild(self):
        try:
            guild_mem = GuildMember.objects.get(character=self)
            return guild_mem.guild
        except GuildMember.DoesNotExist:
            return None


class CharacterJob(models.Model):
    base = models.ForeignKey('rom.CharacterBase', db_index=True)
    job = models.ForeignKey('rom.Job', db_index=True)
    image = models.ImageField(upload_to='rom/character/', blank=True, null=True, default=None)
    status = models.IntegerField(choices=CHARACTER_STATUS, db_index=True, default=1)
    create_timestamp = models.DateTimeField(auto_now_add=True)


