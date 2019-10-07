from django.contrib import admin
from rom.models import *


class JobAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'image', 'sort')


class CharacterBaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ign', 'member', 'base_level', 'contribution', 'gold_medal')


class CharacterJobAdmin(admin.ModelAdmin):
    list_display = ('pk', 'base', 'job', 'image')
    list_filter = ('job', )


admin.site.register(Job, JobAdmin)
admin.site.register(CharacterBase, CharacterBaseAdmin)
admin.site.register(CharacterJob, CharacterJobAdmin)
