# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from jgm.services.request_management import RequestManagement


@login_required()
def get_list(request):
    pass


@login_required()
def create(request):
    pass


@login_required()
def edit(request):
    pass

