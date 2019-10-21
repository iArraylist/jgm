# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rom.models import CharacterBase, CharacterJob, Job
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

    def push_base(self, ign, base_level, contribution, gold_medal, job_ids, hash_form):
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

        for job_id in job_ids:
            self.push_job(
                job_id=job_id,
            )
        return self.base

    def push_job(self, job_id):
        if self.base is not None:
            if not self.base.check_job(job_id=job_id):
                job = CharacterJob(
                    base=self.base,
                    job_id=job_id,
                )
                job.save()
                return job
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def get_base(self):
        if self.base is not None:
            return self.__base_dto(self.base)
        else:
            raise Exception("Please init CharacterManagement with base_id")

    def get_bases(self):
        bases = list()
        bases_obj = CharacterBase.objects.filter(member=self.user)
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

        jobs_obj = base.get_jobs()
        jobs = []
        for j in jobs_obj:
            job = dict()
            job['id'] = j.pk
            job['job_id'] = j.job.pk
            job['job_name'] = j.job.name
            job['job_image'] = j.job.image
            jobs.append(job)

        base_dto['jobs'] = jobs

        guild_obj = base.get_guild()
        if guild_obj is not None:
            guild = dict()
            guild['guild_id'] = guild_obj.id
            guild['guild_name'] = guild_obj.name
            guild['guild_image'] = guild_obj.image
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
