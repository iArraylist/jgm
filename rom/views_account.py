# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import HttpResponse


def logout(request):
    django_logout(request)
    try:
        return redirect('rom_home')
    except:
        return redirect(settings.URL_SITE)


def login(request):
    if request.user.is_authenticated():
        return redirect('rom_home')

    if request.method == 'POST':
        return HttpResponse("MA")
    else:
        return HttpResponse("MA")


def register(request):
    return HttpResponse("MA")