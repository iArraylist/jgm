from django.conf.urls import url
from . import views as rom_views
from . import views_account as rom_views_account

urlpatterns = [
    url(r'^$', rom_views.home, name='rom_home'),
    url(r'^logout/$', rom_views_account.logout, name='rom_logout'),
    url(r'^login/$', rom_views_account.login, name='rom_login'),
]