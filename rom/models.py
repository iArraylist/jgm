# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from guild.models import GuildMember
import json

CHARACTER_STATUS = (
    (0, 'Inactive'),
    (1, 'Active'),
)


class Job(models.Model):
    name = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='rom/class/', blank=True, null=True, default=None)
    sort = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['sort']

    def __str__(self):
        return self.name


class CharacterBase(models.Model):
    member = models.ForeignKey('auth.User', db_index=True, related_name='bases', related_query_name='base')
    ign = models.CharField(max_length=255, db_index=True)
    base_level = models.PositiveSmallIntegerField(default=1, db_index=True)
    contribution = models.PositiveIntegerField(default=0, db_index=True)
    gold_medal = models.PositiveIntegerField(default=0, db_index=True)
    status = models.IntegerField(choices=CHARACTER_STATUS, db_index=True, default=1)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    data = models.TextField(default='null')

    def __str__(self):
        return '%s_%s' % (self.member.pk, self.ign)

    def check_job(self, job_id):
        if self.jobs.filter(job_id=job_id).exists():
            return True
        return False

    def get_data_json(self, key=None, default=None):
        try:
            data_json = json.loads(self.data)
            if data_json is None:
                data_json = {}
        except ValueError:
            data_json = {}
        if key is not None:
            if key in data_json:
                return data_json[key]
            else:
                return default
        return data_json

    def update_data(self, data_dict):
        data = self.get_data_json()
        data.update(data_dict)
        data_json = data
        self.data = json.dumps(data)
        return data_json


class CharacterJob(models.Model):
    base = models.ForeignKey('rom.CharacterBase', db_index=True, related_name='jobs', related_query_name='job')
    job = models.ForeignKey('rom.Job', db_index=True)
    image = models.ImageField(upload_to='rom/character/', blank=True, null=True, default=None)
    status = models.IntegerField(choices=CHARACTER_STATUS, db_index=True, default=1)
    create_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('base', 'job'),)

    def __str__(self):
        return '%s_%s' % (self.base.ign, self.job.name)


class Profile(models.Model):
    member = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
    line_contact = models.CharField(max_length=50, default='')
    nickname = models.CharField(max_length=50, default='')

    def __str__(self):
        return 'profile_%s' % self.member.pk
