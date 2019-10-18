# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from jgm.services.request_management import RequestManagement
from rom.services.character_management import CharacterManagement
from rom.form_character import CharacterForm
from rom.models import Job


@login_required()
def create(request):
    rm = RequestManagement(request)

    if rm.is_method_post():
        form = CharacterForm(request.POST)
        if form.is_valid():
            form_json = form.cleaned_data
            print form_json
            chm = CharacterManagement(rm.get_user())
            chm.push_base(ign=form_json['ign'],
                          base_level=form_json['base_level'],
                          contribution=form_json['contribution'],
                          gold_medal=form_json['gold_medal'],
                          job_ids=form_json['jobs'])
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

    if rm.is_method_get():
        context = dict()
        context['submit_url'] = reverse('rom_character_edit', args=[base_id])
        return render(request, 'character.html', context=context)
    elif rm.is_method_post():
        chm = CharacterManagement(rm.get_user(), base_id=base_id)

