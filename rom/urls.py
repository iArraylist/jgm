from django.conf.urls import url, include
from . import views as rom_views, views_character as rom_views_character
from guild import views as guild_views
from jgm import views_account as jgm_views_account
from party import views as party_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', rom_views.home, name='rom_home'),

    url(r'^logout/$', jgm_views_account.logout, name='rom_logout'),
    url(r'^login/$', jgm_views_account.login, name='rom_login'),
    url('social-auth/', include('social_django.urls', namespace='social')),

    url(r'^character/create/$', rom_views_character.create, name='rom_character_create'),
    url(r'^character/(\d+)/$', rom_views_character.edit, name='rom_character_edit'),
    url(r'^character/(\d+)/del/$', rom_views_character.delete, name='rom_character_del'),
    url(r'^character/(\d+)/guild/create/$', guild_views.create, name='guild_create'),
    url(r'^character/(\d+)/guild/join/(\w+)/$', guild_views.join, name='guild_join'),

    url(r'^join/(\w+)/$', guild_views.join_landing, name='guild_join_landing'),

    url(r'^guild/(\w+)/waiting-list/$', guild_views.waiting_list, name='guild_waiting_list'),
    url(r'^guild/(\w+)/approve/(\d+)/$', guild_views.approve, name='guild_approve'),
    url(r'^guild/(\w+)/reject/(\d+)/$', guild_views.reject, name='guild_reject'),
    url(r'^guild/(\w+)/fire/(\d+)/$', guild_views.fire, name='guild_fire'),
    url(r'^guild/(\w+)/$', guild_views.home, name='guild_home'),

    url(r'^guild/(\w+)/party/(\w+)/summary/$', party_views.party_summary, name='guild_party_summary'),
    url(r'^guild/(\w+)/party/(\w+)/$', party_views.party_list, name='guild_party_list'),
    url(r'^guild/(\w+)/party/(\w+)/edit/$', party_views.party_edit_list, name='guild_party_edit_list'),
    url(r'^guild/(\w+)/party/(\w+)/add/$', party_views.party_add, name='guild_party_add'),
    url(r'^guild/(\w+)/party/(\w+)/del/$', party_views.party_del, name='guild_party_del'),
    url(r'^guild/(\w+)/party/(\w+)/get_war_jobs/$', party_views.get_war_jobs, name='guild_party_get_war_jobs'),
    url(r'^guild/(\w+)/party/(\w+)/push_war_job/$', party_views.push_war_job, name='guild_party_push_war_job'),
    url(r'^guild/(\w+)/party/(\w+)/push_leader/$', party_views.push_leader, name='guild_party_push_leader'),
    url(r'^guild/(\w+)/party/(\w+)/push_party_data/$', party_views.push_party_data, name='guild_party_push_party_data'),
    url(r'^guild/(\w+)/party/(\w+)/clb/$', party_views.check_left_behind, name='guild_party_check_left_behind'),

    url(r'profile/save/$', rom_views.profile_save, name='profile_save')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)