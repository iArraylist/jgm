# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rom.models import Job
from guild.models import Guild
from party.models import Party, PartyMember
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.db.models import Q, Max


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
                    nickname = m.war_job.character.member.profile.nickname
                except AttributeError:
                    war_job_id = None
                    ign = None
                    job_id = None
                    nickname = None
                member['id'] = m.pk
                member['data'] = m.get_data_json()
                member['war_job_id'] = war_job_id
                member['ign'] = ign
                member['nickname'] = nickname
                member['job_id'] = job_id
                party['member'].append(member)
            party_list.append(party)
        return party_list

    def get_summary(self):
        war_job_wp_q = self.guild.member_war_jobs.filter(war=self.WAR_TYPE, party_m__isnull=False).order_by('job__sort', 'character__ign')
        war_job_wp = dict()
        war_job_wp_list = list()
        wp_total = 0
        for job in Job.objects.all():
            war_job_wp_filter_job = war_job_wp_q.filter(job=job)
            dto = dict()
            dto['job_name'] = job.name
            dto['job_image'] = job.image.url
            chl = list()
            for war_job in war_job_wp_filter_job:
                ch_dto = dict()
                ch_dto['ign'] = war_job.character.ign
                ch_dto['nickname'] = war_job.character.member.profile.nickname
                chl.append(ch_dto)
            dto['total'] = len(war_job_wp_filter_job)
            dto['character_list'] = chl
            wp_total = wp_total + dto['total']
            war_job_wp_list.append(dto)
        war_job_wp['total'] = wp_total
        war_job_wp['list'] = war_job_wp_list

        war_job_wop_q = self.guild.member_war_jobs.filter(war=self.WAR_TYPE, party_m__isnull=True).order_by('job__sort', 'character__ign')
        war_job_wop = dict()
        war_job_wop_list = list()
        wop_total = 0
        for war_job in war_job_wop_q:
            ch_dto = dict()
            ch_dto['ign'] = war_job.character.ign
            ch_dto['nickname'] = war_job.character.member.profile.nickname
            ch_dto['job'] = dict()
            if war_job.job:
                ch_dto['job']['job_name'] = war_job.job.name
                ch_dto['job']['job_image'] = war_job.job.image.url
            else:
                ch_dto['job']['job_name'] = None
                ch_dto['job']['job_image'] = None
            wop_total = wop_total + 1
            war_job_wop_list.append(ch_dto)
        war_job_wop['total'] = wop_total
        war_job_wop['list'] = war_job_wop_list
        return war_job_wp, war_job_wop

    def left_behind(self):
        return self.guild.member_war_jobs.filter(war=self.WAR_TYPE, party_m__isnull=True).exists()

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

    def push(self):
        plist = Party.objects.filter(guild=self.guild, war=self.WAR_TYPE)
        sort = plist.aggregate(Max('sort')).get('sort__max') + 1 if plist.aggregate(Max('sort')).get('sort__max') is not None else 1
        name = 'P.%s' % (len(plist) + 1)
        party = Party(
            guild=self.guild,
            war=self.WAR_TYPE,
            name=name,
            sort=sort
        )
        data = dict()
        data['remark'] = ''
        data['color'] = 'def'
        party.update_data(data)
        party.save()
        for pm_sort in range(6):
            pm = PartyMember(
                party=party,
                sort=pm_sort
            )
            pm_data = dict()
            pm_data['leader'] = False
            pm.update_data(pm_data)
            pm.save()

    def delete(self):
        error_code = 0
        self.party.delete()
        return error_code

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
        data = dict()
        data['leader'] = check
        self.party_member.update_data(data_dict=data)
        self.party_member.save()
        return error_code

    def push_data(self, party_name, data):
        error_code = 0
        self.party.name = party_name
        self.party.update_data(data)
        self.party.save()
        return error_code


class WOEManagement(PartyManagement):
    WAR_TYPE = 0
    WAR_NAME = 'WOE'


class WOCManagement(PartyManagement):
    WAR_TYPE = 1
    WAR_NAME = 'WOC'


class ZoneManagement(PartyManagement):
    WAR_TYPE = 2
    WAR_NAME = 'ZONE'


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
