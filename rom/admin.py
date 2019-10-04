from django.contrib import admin
from rom.models import *


class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'sort')


admin.site.register(Class, ClassAdmin)
