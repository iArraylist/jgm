# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rom.models import CharacterBase
from guild.form_guild import GuildCreateForm
from guild.models import Guild, GuildMember
from jgm.services.request_management import get_data


class GuildCreateManagement(object):
    def __init__(self, user, base_id):
        self.user = user
        try:
            self.base = CharacterBase.objects.get(pk=base_id, member=self.user)
        except CharacterBase.DoesNotExist:
            raise Exception('%s DoesNotExist' % base_id)
        guild_m = self.base.guild.first()
        if guild_m:
            raise Exception('%s already join %s' % (self.base.ign, guild_m.guild.name))

    def push(self, form_json):
        name = form_json['name']
        line_contact = form_json['line_contact']
        guild = Guild(name=name,
                      invite_code=None)
        data = get_data(form_json, ['discord_link'])
        guild.update_data(data_dict=data)

        guild.save()
        guild_member = GuildMember(
            guild=guild,
            character=self.base,
            line_contact=line_contact,
            role=0)
        guild_member.save()

    def get_form(self):
        return self.__generate_form()

    def __generate_form(self):
        initial = dict()
        initial['character'] = self.base.ign
        form = GuildCreateForm(initial=initial)
        return form

