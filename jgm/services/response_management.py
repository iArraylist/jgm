# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from guild.models import GuildMember, Guild


class ResponseManagement(object):
    def __init__(self, request):
        self.request = request
        self.user = self.request.user

    def gen_menu_context(self, stage='dashboard'):
        menu = dict()
        menu['on_stage'] = stage
        menu_list = list()
        m = dict()
        m['text'] = 'Dashboard'
        m['stage'] = 'dashboard'
        m['url'] = reverse('rom_home')
        menu_list.append(m)
        guilds = GuildMember.objects.filter(role__in=[0, 1, 2], character__member=self.user).values('guild').distinct()
        for g in guilds:
            guild = Guild.objects.get(pk=g['guild'])
            m = dict()
            m['text'] = guild.name
            m['stage'] = 'guild'
            m['url'] = reverse('guild_home', args=[guild.invite_code])
            menu_list.append(m)

            m = dict()
            m['text'] = '%s [%s]' % (guild.name, 'WOE')
            m['stage'] = 'woe'
            m['url'] = reverse('guild_party_list', args=[guild.invite_code, 'woe'])
            menu_list.append(m)

            m = dict()
            m['text'] = '%s [%s]' % (guild.name, 'WOC')
            m['stage'] = 'woc'
            m['url'] = reverse('guild_party_list', args=[guild.invite_code, 'woc'])
            menu_list.append(m)

            m = dict()
            m['text'] = '%s [%s]' % (guild.name, 'ZONE')
            m['stage'] = 'zone'
            m['url'] = reverse('guild_party_list', args=[guild.invite_code, 'zone'])
            menu_list.append(m)

        menu['list'] = menu_list
        return menu
