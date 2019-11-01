# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import json
from django.http import HttpResponse
from jgm.services.request_management import RequestManagement
from party.services.party_management import PartyService
from rom.models import Job
from rom.views import job_images, jobs


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


@login_required
def party_edit_list(request, invite_code, war_type):
    rm = RequestManagement(request)
    service = PartyService(rm.get_user(), invite_code=invite_code, war_type=war_type, allow_role=[0, 1]).get()
    party = service.get_party_list()
    war_name = service.get_war_name()
    context = dict()
    context['party_list'] = party
    context['war'] = {'war_name': war_name, 'war_type': war_type}
    context['invite_code'] = invite_code
    context['job_images'] = job_images
    context['jobs'] = jobs
    context['edit'] = True
    return render(request, 'party/list.html', context=context)


@csrf_exempt
@login_required
def get_war_jobs(request, invite_code, war_type):
    rm = RequestManagement(request)
    p_id = request.GET.get('p_id')
    pm_id = request.GET.get('pm_id')
    job_id = request.GET.get('job_id', 'None')
    war_job_id_selected = request.GET.get('war_job_id_selected', 'None')
    service = PartyService(rm.get_user(), invite_code=invite_code, war_type=war_type, allow_role=[0, 1], p_id=p_id, pm_id=pm_id).get()
    res = dict()
    res['result'] = service.get_war_jobs(job_id=job_id, war_job_id_selected=war_job_id_selected)
    response = HttpResponse(json.dumps(res), content_type='application/json; charset=UTF-8')
    return response


@csrf_exempt
@login_required
def push_war_job(request, invite_code, war_type):
    rm = RequestManagement(request)
    p_id = request.GET.get('p_id')
    pm_id = request.GET.get('pm_id')
    war_job_id = request.GET.get('war_job_id', 'None')
    service = PartyService(rm.get_user(), invite_code=invite_code, war_type=war_type, allow_role=[0, 1], p_id=p_id, pm_id=pm_id).get()
    res = dict()
    res['error_code'] = service.push_war_job(war_job_id=war_job_id)
    response = HttpResponse(json.dumps(res), content_type='application/json; charset=UTF-8')
    return response


@csrf_exempt
@login_required
def push_leader(request, invite_code, war_type):
    rm = RequestManagement(request)
    p_id = request.GET.get('p_id')
    pm_id = request.GET.get('pm_id')
    check = request.GET.get('check', False)
    service = PartyService(rm.get_user(), invite_code=invite_code, war_type=war_type, allow_role=[0, 1], p_id=p_id, pm_id=pm_id).get()
    res = dict()
    res['error_code'] = service.push_leader(check=check)
    response = HttpResponse(json.dumps(res), content_type='application/json; charset=UTF-8')
    return response
