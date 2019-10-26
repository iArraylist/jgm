# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from jgm.services.request_management import RequestManagement
from party.services.party_management import PartyService
from rom.models import Job
from rom.views import job_images


@login_required
def party_list(request, invite_code, war_type):
    rm = RequestManagement(request)
    service = PartyService(rm.get_user(), invite_code=invite_code, war_type=war_type, allow_role=[0, 1, 2]).get()
    party = service.get_party_list()
    war_name = service.get_war_name()
    context = dict()
    context['party_list'] = party
    context['war'] = {'war_name': war_name, 'war_type': war_type}
    context['invite_code'] = invite_code
    context['job_images'] = job_images
    return render(request, 'party/list.html', context=context)


@login_required
def party_summary(request, invite_code, war_type):
    rm = RequestManagement(request)
    service = PartyService(rm.get_user(), invite_code=invite_code, war_type=war_type, allow_role=[0, 1, 2]).get()
    war_name = service.get_war_name()
    context = dict()
    context['war'] = {'war_name': war_name, 'war_type': war_type}
    context['invite_code'] = invite_code
    return render(request, 'party/summary.html', context=context)
