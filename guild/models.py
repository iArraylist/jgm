# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json

MEMBER_ROLE = (
    (0, 'Guild Leader'),
    (1, 'Guild Vice Leader'),
    (2, 'Guild Member')
)


class Guild(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='guild/', blank=True, null=True, default=None)
    data = models.TextField(default='null')
    invite_code = models.CharField(max_length=50, db_index=True, unique=True)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

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

    def generate_invite_code(self):
        import uuid
        gen = True
        while gen:
            code = uuid.uuid4().hex[:6].upper()
            if not Guild.objects.filter(invite_code=code).exists():
                self.invite_code = code
                gen = False


class GuildMember(models.Model):
    guild = models.ForeignKey('guild.Guild', db_index=True, related_name='members', related_query_name='member')
    character = models.ForeignKey('rom.CharacterBase', db_index=True, related_name='guild', related_query_name='guild')
    line_contact = models.CharField(max_length=50)
    role = models.IntegerField(choices=MEMBER_ROLE, db_index=True)
