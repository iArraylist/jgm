# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from guild.models import Guild
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.db.models import Q


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
            party['id'] = p.pk
            party['name'] = p.name
            party['data'] = p.get_data_json()
            party['member'] = list()
            for m in members:
                member = dict()
                try:
                    war_job_id = m.war_job.pk
                    ign = m.war_job.character.ign
                    job_id = m.war_job.job.pk
                except AttributeError:
                    war_job_id = None
                    ign = None
                    job_id = None
                member['id'] = m.pk
                member['data'] = m.get_data_json()
                member['war_job_id'] = war_job_id
                member['name'] = ign
                member['job_id'] = job_id
                party['member'].append(member)
            party_list.append(party)
        return party_list

    def get_war_name(self):
        return self.WAR_NAME

    def get_war_jobs(self, pm_id, job_id):
        war_job_list_q = self.guild.member_war_jobs.filter(Q(party_m__id=pm_id) | Q(party_m__isnull=True), job_id=job_id, war=self.WAR_TYPE)
        war_job_list = list()
        for war_job in war_job_list_q:
            war_job_list.append((war_job.pk, war_job.character.ign))
        return war_job_list


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
