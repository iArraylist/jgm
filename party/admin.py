# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from party.models import *


class PartyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'guild', 'war', 'name', 'sort')
    list_filter = ('guild', 'war',)


class PartyMemberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'party', 'war_job', 'sort')
    list_filter = ('party',)


admin.site.register(Party, PartyAdmin)
admin.site.register(PartyMember, PartyMemberAdmin)
