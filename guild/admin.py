# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from guild.models import *


class GuildAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'image', 'create_timestamp', 'update_timestamp')


class GuildMemberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'guild', 'character', 'role')
    list_filter = ('guild',)


class WaitingApproveAdmin(admin.ModelAdmin):
    list_display = ('pk', 'guild', 'character')
    list_filter = ('guild',)


class WarJobAdmin(admin.ModelAdmin):
    list_display = ('pk', 'guild', 'character', 'job', 'war')
    list_filter = ('guild', 'job',)


admin.site.register(Guild, GuildAdmin)
admin.site.register(GuildMember, GuildMemberAdmin)
admin.site.register(WaitingApprove, WaitingApproveAdmin)
admin.site.register(WarJob, WarJobAdmin)