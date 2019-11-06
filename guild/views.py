# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from jgm.services.request_management import RequestManagement
from guild.services.guild_management import GuildCreateManagement, GuildManagement
from guild.form_guild import GuildCreateForm
from rom.services.character_management import CharacterManagement


@login_required
def create(request, base_id):
    rm = RequestManagement(request)
    chm = CharacterManagement(rm.get_user(), base_id=base_id)
    gcm = GuildCreateManagement(rm.get_user(), base=chm.base)
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
    gam = GuildManagement(rm.get_user(), invite_code=invite_code)
    bases = chm.get_bases(filter_list=[('join_guild', gam.guild)])

    context = dict()
    context['bases'] = bases
    context['invite_code'] = invite_code
    context['guild_info'] = gam.get_guild()
    return render(request, 'guild/join.html', context=context)


@login_required
def join(request, base_id, invite_code):
    rm = RequestManagement(request)
    chm = CharacterManagement(rm.get_user(), base_id=base_id)
    gam = GuildManagement(rm.get_user(), invite_code=invite_code)
    gam.join_waiting(base=chm.base)
    return redirect('rom_home')


@login_required
def waiting_list(request, invite_code):
    rm = RequestManagement(request)
    gam = GuildManagement(rm.get_user(), invite_code=invite_code, allow_role=[0, 1])
    bases = gam.get_waiting_list()
    context = dict()
    context['bases'] = bases
    context['invite_code'] = invite_code
    context['guild_info'] = gam.get_guild()
    return render(request, 'guild/waiting_list.html', context=context)


@login_required
def approve(request, invite_code, base_id):
    rm = RequestManagement(request)
    gam = GuildManagement(rm.get_user(), invite_code=invite_code, allow_role=[0, 1])
    gam.approve(base_id=base_id)
    return redirect('guild_waiting_list', invite_code)


@login_required
def home(request, invite_code):
    rm = RequestManagement(request)
    gam = GuildManagement(rm.get_user(), invite_code=invite_code, allow_role=[0, 1, 2])
    bases = gam.get_members()
    context = dict()
    context['bases'] = bases
    context['invite_code'] = invite_code
    context['guild_info'] = gam.get_guild()
    context['temp_perm'] = gam.temp_perm()
    return render(request, 'guild/home.html', context=context)
