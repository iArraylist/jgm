# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rom.models import CharacterBase, CharacterJob
from rom.form_character import CharacterForm, CharacterWGForm
from django.db.models import Q
from guild.models import WAR_JOB


class CharacterManagement(object):
    def __init__(self, user, base_id=None):
        self.user = user
        if base_id is not None:
            try:
                self.base = CharacterBase.objects.get(pk=base_id, member=self.user)
            except CharacterBase.DoesNotExist:
                raise Exception("%s DoesNotExist" % base_id)
        else:
            self.base = None

    def push_base(self, form_json, hash_form):
        ign = form_json['ign']
        base_level = form_json['base_level']
        contribution = form_json['contribution']
        gold_medal = form_json['gold_medal']
        job_ids = form_json['jobs']

        self.base = CharacterBase(
            member=self.user,
            ign=ign,
            base_level=base_level,
            contribution=contribution,
            gold_medal=gold_medal,
        )

        data = dict()
        data['hash_form'] = hash_form
        self.base.update_data(data_dict=data)
        self.base.save()

        self.__push_jobs(job_ids=job_ids)
        return self.base

    def update_base(self, form_json, hash_form):
        if self.base is not None:
            ign = form_json['ign']
            base_level = form_json['base_level']
            contribution = form_json['contribution']
            gold_medal = form_json['gold_medal']
            job_ids = form_json['jobs']

            self.base.member = self.user
            self.base.ign = ign
            self.base.base_level = base_level
            self.base.contribution = contribution
            self.base.gold_medal = gold_medal

            data = dict()
            data['hash_form'] = hash_form
            self.base.update_data(data_dict=data)
            self.base.save()

            self.__push_jobs(job_ids=job_ids)
            if self.__guild_exists():
                woe = form_json['woe_job']
                woc = form_json['woc_job']
                zone = form_json['zone_job']
                self.__push_war_job(woe=woe, woc=woc, zone=zone)

            return self.base
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def __push_jobs(self, job_ids):
        job_ids = [int(job_id) for job_id in job_ids]
        if self.base is not None:
            job_ids_old = [[job_ch.job.pk, job_ch] for job_ch in self.base.jobs.all()]

            for job_id_old, job_ch in job_ids_old:
                if job_id_old not in job_ids:
                    job_ch.delete()

            for job_id in job_ids:
                self.__push_job(
                    job_id=job_id,
                )
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def __push_job(self, job_id):
        if not self.base.check_job(job_id=job_id):
            job = CharacterJob(
                base=self.base,
                job_id=job_id,
            )
            job.save()
            return job

    def __push_war_job(self, woe, woc, zone):
        war_woe = self.base.guild_war_jobs.filter(war=0).first()
        war_woe.job = self.base.jobs.get(job_id=woe).job
        war_woe.save()
        war_woc = self.base.guild_war_jobs.filter(war=1).first()
        war_woc.job = self.base.jobs.get(job_id=woc).job
        war_woc.save()
        war_zone = self.base.guild_war_jobs.filter(war=2).first()
        war_zone.job = self.base.jobs.get(job_id=zone).job
        war_zone.save()

    def get_base(self):
        if self.base is not None:
            return self.__base_dto(self.base)
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def get_bases(self, filter_list=[]):
        bases = list()
        bases_obj = self.user.bases.all()

        for f, v in filter_list:
            if f == 'join_guild':
                bases_obj = bases_obj.filter(Q(waiting__guild=v) | Q(waiting__isnull=True), guild__isnull=True)

        for b in bases_obj:
            bases.append(self.__base_dto(b))
        return bases

    @staticmethod
    def __base_dto(base):
        base_dto = dict()
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

        guild_m = base.guild.first()
        guild_obj = None
        if guild_m:
            guild_obj = guild_m.guild
        if guild_obj is not None:
            guild = dict()
            guild['guild_id'] = guild_obj.pk
            guild['guild_name'] = guild_obj.name
            guild['guild_image'] = guild_obj.image
            guild['invite_code'] = guild_obj.invite_code
            guild['guild_data'] = guild_obj.get_data_json()
            for war_id, war in WAR_JOB:
                if base.guild_war_jobs.filter(war=war_id).first().job:
                    guild[war] = base.guild_war_jobs.filter(war=war_id).first().job.pk
                else:
                    guild[war] = None
        else:
            guild = None
        base_dto['guild'] = guild

        waiting_approve = base.waiting.first()
        w_guild_obj = None
        if waiting_approve:
            w_guild_obj = waiting_approve.guild
        if w_guild_obj is not None:
            waiting = dict()
            waiting['guild_id'] = w_guild_obj.pk
            waiting['guild_name'] = w_guild_obj.name
            waiting['guild_image'] = w_guild_obj.image
            waiting['invite_code'] = w_guild_obj.invite_code
            waiting['guild_data'] = w_guild_obj.get_data_json()
        else:
            waiting = None
        base_dto['waiting'] = waiting

        return base_dto

    def __guild_exists(self):
        return self.base.guild.all().exists()

    def get_request_form(self, request):
        if self.base is not None:
            if self.__guild_exists():
                return CharacterWGForm(request.POST)
            return CharacterForm(request.POST)
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def get_form_base(self):
        if self.base is not None:
            if self.__guild_exists():
                return self.__generate_form_wg()
            return self.__generate_form()
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def __generate_form(self):
        base_dto = self.get_base()

        initial = dict()
        initial['ign'] = base_dto['ign']
        initial['base_level'] = base_dto['base_level']
        initial['contribution'] = base_dto['contribution']
        initial['gold_medal'] = base_dto['gold_medal']
        job_ids = list()
        for job in base_dto['jobs']:
            job_ids.append(job['job_id'])
        initial['jobs'] = job_ids

        form = CharacterForm(initial=initial)
        return form

    def __generate_form_wg(self):
        base_dto = self.get_base()

        initial = dict()
        initial['ign'] = base_dto['ign']
        initial['base_level'] = base_dto['base_level']
        initial['contribution'] = base_dto['contribution']
        initial['gold_medal'] = base_dto['gold_medal']
        job_ids = list()
        for job in base_dto['jobs']:
            job_ids.append(job['job_id'])
        initial['jobs'] = job_ids
        initial['woe_job'] = base_dto['guild']['woe']
        initial['woc_job'] = base_dto['guild']['woc']
        initial['zone_job'] = base_dto['guild']['zone']

        form = CharacterWGForm(initial=initial)
        return form

    def get_hash_form(self):
        return self.base.get_data_json('hash_form')
