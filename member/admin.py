from django.contrib import admin
from member.models import *


class MemberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'facebook_id', 'email', 'username', 'name')


admin.site.register(Member, MemberAdmin)
