from django.conf.urls import url, patterns, include
from django.contrib import admin


urlpatterns = patterns(
    'jgm',
    url(r'^', include(admin.site.urls)),
)
