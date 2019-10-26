# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json
from guild.models import WAR_TYPE


class Party(models.Model):
    guild = models.ForeignKey('guild.Guild', db_index=True, related_name='party_list', related_query_name='party_list')
    war = models.IntegerField(choices=WAR_TYPE, db_index=True)
    name = models.CharField(max_length=255)
    data = models.TextField(default='null')
    sort = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['sort']
        unique_together = (('guild', 'war', 'sort'),)

    def __str__(self):
        return '%s_%s_%s_%s' % (self.guild.name, WAR_TYPE[self.war][1], self.name, self.sort)

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


class PartyMember(models.Model):
    party = models.ForeignKey('party.Party', db_index=True, related_name='members', related_query_name='member')
    war_job = models.ForeignKey('guild.WarJob', db_index=True, blank=True, null=True, default=None, related_name='party_m_list', related_query_name='party_m')
    data = models.TextField(default='null')
    sort = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['sort']
        unique_together = (('party', 'sort'),)

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
