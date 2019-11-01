# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from guild.models import Guild
from party.models import Party, PartyMember
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.db.models import Q


class PartyManagement(object):
    WAR_TYPE = None
    WAR_NAME = ''

    def __init__(self, guild, party=None, party_member=None):
        self.guild = guild
        self.party = party
        self.party_member = party_member

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

    def get_war_jobs(self, job_id, war_job_id_selected):
        war_job_list = list()
        if job_id != 'None':
            war_job_list_q = self.guild.member_war_jobs.filter(Q(party_m=self.party_member) | Q(party_m__isnull=True), job_id=job_id, war=self.WAR_TYPE)
            for war_job in war_job_list_q:
                war_job_list.append((war_job.pk, war_job.character.ign))
        if war_job_id_selected == 'None':
            if self.party_member.war_job:
                self.party_member.war_job = None
                self.party_member.save()
        return war_job_list

    def push_war_job(self, war_job_id):
        error_code = 0
        if war_job_id != 'None':
            war_job = self.guild.member_war_jobs.get(pk=war_job_id)
            self.party_member.war_job = war_job
            self.party_member.save()
        else:
            self.party_member.war_job = None
            self.party_member.save()
        return error_code

    def push_leader(self, check):
        error_code = 0
        data = {
            'leader': check
        }
        self.party_member.update_data(data_dict=data)
        self.party_member.save()
        return error_code


class WOEManagement(PartyManagement):
    WAR_TYPE = 0
    WAR_NAME = 'WOE'


class WOCManagement(PartyManagement):
    WAR_TYPE = 1
    WAR_NAME = 'WOE'


class ZoneManagement(PartyManagement):
    WAR_TYPE = 2
    WAR_NAME = 'WOE'


class PartyService(object):
    war = {
        'woe': WOEManagement,
        'woc': WOCManagement,
        'zone': ZoneManagement
    }

    def __init__(self, user, invite_code, war_type, allow_role=None, p_id=None, pm_id=None):
        self.user = user
        try:
            self.guild = Guild.objects.get(invite_code=invite_code)
        except Guild.DoesNotExist:
            raise Exception("%s DoesNotExist" % invite_code)
        if allow_role:
            self.__permission(allow_role)
        self.war_type = war_type
        self.party = self.guild.party_list.get(pk=p_id) if p_id is not None else None
        self.party_member = self.party.members.get(pk=pm_id) if pm_id is not None else None
        self.service = self.__get_service(war_type=war_type)

    def __permission(self, allow_role):
        if not self.guild.members.filter(role__in=allow_role, character__member=self.user).exists():
            raise PermissionDenied

    def __get_service(self, war_type):
        try:
            return self.war[war_type](guild=self.guild, party=self.party, party_member=self.party_member)
        except KeyError:
            raise Http404

    def get(self):
        return self.service
