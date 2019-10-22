# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rom.models import CharacterBase
from guild.form_guild import GuildCreateForm
from guild.models import Guild, GuildMember, WaitingApprove
from jgm.services.request_management import get_data


class GuildCreateManagement(object):
    def __init__(self, user, base):
        self.user = user
        self.base = base
        guild_m = self.base.guild.first()
        if guild_m:
            raise Exception('%s already join %s' % (self.base.ign, guild_m.guild.name))

    def push(self, form_json):
        name = form_json['name']
        guild = Guild(name=name,
                      invite_code=None)
        data = get_data(form_json, ['discord_link'])
        guild.update_data(data_dict=data)

        guild.save()
        guild_member = GuildMember(
            guild=guild,
            character=self.base,
            role=0)
        guild_member.save()

    def get_form(self):
        return self.__generate_form()

    def __generate_form(self):
        initial = dict()
        initial['character'] = self.base.ign
        form = GuildCreateForm(initial=initial)
        return form


class GuildManagement(object):
    def __init__(self, user, invite_code):
        self.user = user
        try:
            self.guild = Guild.objects.get(invite_code=invite_code)
        except Guild.DoesNotExist:
            raise Exception("%s DoesNotExist" % invite_code)

    def get_guild(self):
        guild = dict()
        guild['id'] = self.guild.pk
        guild['name'] = self.guild.name
        guild['data'] = self.guild.get_data_json()
        return guild

    def join_waiting(self, base):
        waiting = WaitingApprove(
            guild=self.guild,
            character=base
        )
        waiting.save()
        return waiting
