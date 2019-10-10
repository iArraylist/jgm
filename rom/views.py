# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from jgm.services.request_management import RequestManagement
from rom.services.character_management import CharacterManagement


@login_required
def home(request):
    rm = RequestManagement(request)
    chm = CharacterManagement(rm.get_user())
    bases = chm.get_bases()

    context = dict()
    context['bases'] = bases
    return render(request, 'home.html', context=context)
