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
            chm = CharacterManagement(rm.get_user())
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

