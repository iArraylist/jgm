# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from jgm.services.request_management import RequestManagement
from guild.services.guild_management import GuildCreateManagement
from guild.form_guild import GuildCreateForm
from rom.services.character_management import CharacterManagement


@login_required
def create(request, base_id):
    rm = RequestManagement(request)
    gcm = GuildCreateManagement(rm.get_user(), base_id=base_id)
    if rm.is_method_post():
        form = GuildCreateForm(request.POST)
        print form
        if form.is_valid():
            form_json = form.cleaned_data
            gcm.push(form_json=form_json)
            return redirect('rom_home')
    else:
        form = gcm.get_form()

    context = dict()
    context['submit_url'] = reverse('guild_create', args=[base_id])
    context['form'] = form
    return render(request, 'guild/create.html', context=context)


@login_required
def join_landing(request, invite_code):
    rm = RequestManagement(request)
    chm = CharacterManagement(rm.get_user())
    bases = chm.get_bases(filter_list=['join_guild'])

    context = dict()
    context['bases'] = bases
    context['invite_code'] = invite_code
    return render(request, 'guild/join.html', context=context)


@login_required()
def join(request, base_id, invite_code):
    return redirect('rom_home')
