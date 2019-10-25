# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from guild.models import Guild
from django.core.exceptions import PermissionDenied
from django.http import Http404

class Party(object):
    WAR_TYPE = None
    WAR_NAME = ''

    def __init__(self, guild):
        self.guild = guild

    def get_party_list(self):
        party_list_q = self.guild.party_list.filter(war=self.WAR_TYPE)
        party_list = list()
        for p in party_list_q:
            members = p.members.all()
            party = dict()
            party_data = p.get_data_json()
            party['name'] = party_data['name']
            party['member'] = list()
            for m in members:
                member = dict()
                try:
                    ign = m.war_job.character.ign
                    job_name = m.war_job.job.name
                except AttributeError:
                    ign = None
                    job_name = None
                member['name'] = ign
                member['job'] = job_name
                party['member'].append(member)
            party_list.append(party)
        return party_list

    def get_war_name(self):
        return self.WAR_NAME


class WOEManagement(Party):
    WAR_TYPE = 0
    WAR_NAME = 'WOE'


class WOCManagement(Party):
    WAR_TYPE = 1
    WAR_NAME = 'WOE'


class ZoneManagement(Party):
    WAR_TYPE = 2
    WAR_NAME = 'WOE'


class PartyService(object):
    war = {
        'woe': WOEManagement,
        'woc': WOCManagement,
        'zone': ZoneManagement
    }

    def __init__(self, user, invite_code, war_type, allow_role=None):
        self.user = user
        try:
            self.guild = Guild.objects.get(invite_code=invite_code)
        except Guild.DoesNotExist:
            raise Exception("%s DoesNotExist" % invite_code)
        if allow_role:
            self.__permission(allow_role)
        self.war_type = war_type
        self.service = self.__get_service(war_type=war_type)

    def __permission(self, allow_role):
        if not self.guild.members.filter(role__in=allow_role, character__member=self.user).exists():
            raise PermissionDenied

    def __get_service(self, war_type):
        try:
            return self.war[war_type](guild=self.guild)
        except KeyError:
            raise Http404

    def get(self):
        return self.service
