# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from jgm.services.request_management import RequestManagement
from jgm.services.response_management import ResponseManagement
from rom.services.character_management import CharacterManagement
from rom.services.profile_mangement import ProfileManagement
from rom.form_profile import ProfileForm
from rom.models import Job

job_images = {job.pk: job.image.url for job in Job.objects.all()}
jobs = [(job.pk, job.name) for job in Job.objects.all()]


@login_required
def home(request):
    rm = RequestManagement(request)
    chm = CharacterManagement(rm.get_user())
    bases = chm.get_bases()

    pm = ProfileManagement(rm.get_user())
    form_profile = pm.get_form()

    context = dict()
    context['form_profile'] = form_profile
    context['bases'] = bases
    rp = ResponseManagement(request)
    context['menu'] = rp.gen_menu_context(stage='dashboard')
    return render(request, 'home.html', context=context)


@login_required
def profile_save(request):
    rm = RequestManagement(request)
    if rm.is_method_post():
        form = ProfileForm(request.POST)
        if form.is_valid():
            form_json = form.cleaned_data
            pm = ProfileManagement(rm.get_user())
            pm.update(form_json)

    return redirect('rom_home')


