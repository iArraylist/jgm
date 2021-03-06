# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.http import HttpResponse
from django.shortcuts import render
from jgm.services.request_management import RequestManagement


def logout(request):
    django_logout(request)
    return redirect('rom_home')


def login(request):
    rm = RequestManagement(request)
    if rm.is_authenticated():
        return redirect('rom_home')

    return render(request, 'registration/login.html')


def register(request):
    return HttpResponse("MA")
