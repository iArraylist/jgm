# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


MEMBER_ROLE = (
    (0, 'Guild Leader'),
    (1, 'Guild Vice Leader'),
    (2, 'Guild Member')
)


class Guild(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='guild/', blank=True, null=True, default=None)
    data = models.TextField(blank=True, null=True, default=None)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)


class GuildMember(models.Model):
    guild = models.ForeignKey('guild.Guild', db_index=True)
    character = models.ForeignKey('rom.CharacterBase', db_index=True)
    role = models.IntegerField(choices=MEMBER_ROLE, db_index=True)