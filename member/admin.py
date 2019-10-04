from django.contrib import admin
from member.models import *


class MemberAdmin(admin.ModelAdmin):
    list_display = ('facebook_id', 'email', 'username', 'name')
    list_filter = ('facebook_id', 'email', 'username', 'name')


admin.site.register(Member, MemberAdmin)
