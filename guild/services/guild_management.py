# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rom.models import CharacterBase
from guild.form_guild import GuildCreateForm
from guild.models import Guild, GuildMember, WaitingApprove, WAR_TYPE, WarJob
from jgm.services.request_management import get_data

from rom.services.profile_mangement import ProfileManagement
from django.core.exceptions import PermissionDenied


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
        data = get_data(form_json, [('discord_link', None)])
        guild.update_data(data_dict=data)

        guild.save()
        guild_member = GuildMember(
            guild=guild,
            character=self.base,
            role=0)
        guild_member.save()

        for war_id, war in WAR_TYPE:
            war = WarJob(
                guild=guild,
                character=self.base,
                war=war_id)
            war.save()

    def get_form(self):
        return self.__generate_form()

    def __generate_form(self):
        initial = dict()
        initial['character'] = self.base.ign
        form = GuildCreateForm(initial=initial)
        return form


class GuildManagement(object):
    def __init__(self, user, invite_code, allow_role=None):
        self.user = user
        try:
            self.guild = Guild.objects.get(invite_code=invite_code)
        except Guild.DoesNotExist:
            raise Exception("%s DoesNotExist" % invite_code)
        if allow_role:
            self.__permission(allow_role)

    def __permission(self, allow_role):
        if not self.guild.members.filter(role__in=allow_role, character__member=self.user).exists():
            raise PermissionDenied

    def temp_perm(self):
        if not self.guild.members.filter(role__in=[0, 1], character__member=self.user).exists():
            return False
        return True

    def get_waiting_list(self):
        wa = self.guild.waiting_list.all()
        bases = list()
        for w in wa:
            bases.append(self.__base_dto(w.character))
        return bases

    def get_w_bases(self):
        if self.guild.waiting_list.first():
            return True
        return False

    def approve(self, base_id):
        base = self.__get_base(base_id)
        if self.guild.waiting_list.filter(character=base).exists():
            guild_member = GuildMember(
                guild=self.guild,
                character=base,
                role=2)
            guild_member.save()
            for war_id, war in WAR_TYPE:
                war = WarJob(
                    guild=self.guild,
                    character=base,
                    war=war_id)
                war.save()
            self.guild.waiting_list.filter(character=base).delete()
        else:
            raise Exception("Missing request")

    def reject(self, base_id):
        self.guild.waiting_list.filter(character_id=base_id).delete()

    def fire(self, base_id):
        self.guild.members.filter(character_id=base_id).delete()
        self.guild.member_war_jobs.filter(character_id=base_id).delete()
        return 0

    def get_guild(self):
        guild = dict()
        guild['id'] = self.guild.pk
        guild['name'] = self.guild.name
        guild['data'] = self.guild.get_data_json()
        return guild

    def join_waiting(self, base):
        if not base.waiting.exists() and not base.guild.exists():
            waiting = WaitingApprove(
                guild=self.guild,
                character=base
            )
            waiting.save()
        else:
            raise Exception("Cannot join %s you are already in guild approve waiting list or guild(?) member" % self.guild.name)

    def get_members(self):
        guild_m = self.guild.members.all()
        bases = list()
        for gm in guild_m:
            bases.append(self.__base_dto(gm.character))
        return bases

    @staticmethod
    def __get_base(base_id):
        try:
            base = CharacterBase.objects.get(pk=base_id)
        except CharacterBase.DoesNotExist:
            raise Exception("%s DoesNotExist" % base_id)
        return base

    def __base_dto(self, base):
        base_dto = dict()
        if base.member == self.user:
            base_dto['owner'] = True
        else:
            base_dto['owner'] = False

        base_dto['id'] = base.pk
        base_dto['ign'] = base.ign
        base_dto['base_level'] = base.base_level
        base_dto['contribution'] = base.contribution
        base_dto['gold_medal'] = base.gold_medal

        jobs_ch = base.jobs.all()
        jobs = []
        for j in jobs_ch:
            job = dict()
            job['id'] = j.pk
            job['job_id'] = j.job.pk
            job['job_name'] = j.job.name
            job['job_image'] = j.job.image
            jobs.append(job)

        base_dto['jobs'] = jobs
        pm = ProfileManagement(base.member)
        base_dto['profile'] = pm.get()

        if base.guild_war_jobs.all().exists():
            war_job_woe = base.guild_war_jobs.get(war=0)
            woe = dict()
            woe['id'] = war_job_woe.pk
            if war_job_woe.job:
                woe['job_name'] = war_job_woe.job.name
                woe['job_image'] = war_job_woe.job.image.url
            else:
                woe['job_name'] = None
                woe['job_image'] = None
            base_dto['war_job_woe'] = woe

            war_job_woc = base.guild_war_jobs.get(war=1)
            woc = dict()
            woc['id'] = war_job_woc.pk
            if war_job_woc.job:
                woc['job_name'] = war_job_woc.job.name
                woc['job_image'] = war_job_woc.job.image.url
            else:
                woc['job_name'] = None
                woc['job_image'] = None
            base_dto['war_job_woc'] = woc

            war_job_zone = base.guild_war_jobs.get(war=2)
            zone = dict()
            zone['id'] = war_job_zone.pk
            if war_job_zone.job:
                zone['job_name'] = war_job_zone.job.name
                zone['job_image'] = war_job_zone.job.image.url
            else:
                zone['job_name'] = None
                zone['job_image'] = None
            base_dto['war_job_zone'] = zone

        return base_dto

