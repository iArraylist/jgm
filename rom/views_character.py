# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from jgm.services.request_management import RequestManagement
from rom.services.character_management import CharacterManagement
from rom.form_character import CharacterForm
from rom.models import Job
import json, hashlib


@login_required()
def create(request):
    rm = RequestManagement(request)

    if rm.is_method_post():
        form = CharacterForm(request.POST)
        if form.is_valid():
            form_json = form.cleaned_data
            dmp = json.dumps(form_json)
            hash_form = hashlib.md5(dmp.encode("utf-8")).hexdigest()
            chm = CharacterManagement(rm.get_user())
            chm.push_base(form_json=form_json,
                          hash_form=hash_form)
            return redirect('rom_home')
    else:
        form = CharacterForm()

    job_images = {job.pk: job.image.url for job in Job.objects.all()}

    context = dict()
    context['submit_url'] = reverse('rom_character_create')
    context['form'] = form
    context['job_images'] = job_images
    return render(request, 'character.html', context=context)


@login_required()
def edit(request, base_id):
    rm = RequestManagement(request)
    error_change = None

    chm = CharacterManagement(rm.get_user(), base_id=base_id)

    if rm.is_method_post():
        form = CharacterForm(request.POST)
        if form.is_valid():
            form_json = form.cleaned_data
            dmp = json.dumps(form_json)
            hash_form = hashlib.md5(dmp.encode("utf-8")).hexdigest()
            hash_form_old = chm.get_hash_form()
            if hash_form != hash_form_old:
                chm.update_base(form_json=form_json,
                                hash_form=hash_form)
                return redirect('rom_home')
            error_change = "Please, update your character info."
    else:
        form = chm.get_form_base()

    job_images = {job.pk: job.image.url for job in Job.objects.all()}

    context = dict()
    context['submit_url'] = reverse('rom_character_edit', args=[base_id])
    context['form'] = form
    context['job_images'] = job_images
    context['job_ids'] = [job['job_id'] for job in chm.get_base()['jobs']]
    context['error_change'] = error_change
    return render(request, 'character.html', context=context)

