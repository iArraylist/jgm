from django.conf.urls import url, patterns, include
from django.contrib import admin


urlpatterns = patterns(
    'rom',
    url(r'^', 'views.home', name='rom_home'),
    url(r'^home/$', 'views.home', name='rom_home'),
)