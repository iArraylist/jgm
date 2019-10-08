from django.conf.urls import url, include
from . import views as rom_views
from jgm import views_account as jgm_views_account

urlpatterns = [
    url(r'^$', rom_views.home, name='home'),
    url(r'^logout/$', jgm_views_account.logout, name='logout'),
    url(r'^login/$', jgm_views_account.login, name='login'),
    url('social-auth/', include('social_django.urls', namespace='social')),
]