# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rom.models import CharacterBase, CharacterJob
from rom.form_character import CharacterForm


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

    def get_base(self):
        if self.base is not None:
            return self.__base_dto(self.base)
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def get_bases(self, filter_list=[]):
        bases = list()
        bases_obj = self.user.bases.all()

        for f in filter_list:
            if f == 'join_guild':
                bases_obj = bases_obj.filter(guild__isnull=True)

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
            guild['guild_id'] = guild_obj.id
            guild['guild_name'] = guild_obj.name
            guild['guild_image'] = guild_obj.image
            guild['invite_code'] = guild_obj.invite_code
            guild['guild_data'] = guild_obj.get_data_json()
        else:
            guild = None
        base_dto['guild'] = guild

        return base_dto

    def get_form_base(self):
        if self.base is not None:
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

    def get_hash_form(self):
        return self.base.get_data_json('hash_form')
