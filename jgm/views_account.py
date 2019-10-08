# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def logout(request):
    django_logout(request)
    return redirect('home')


def login(request):
    if request.user.is_authenticated():
        return redirect('home')

    return render(request, 'registration/login.html')


def register(request):
    return HttpResponse("MA")
