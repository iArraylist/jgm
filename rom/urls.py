from django.conf.urls import url, include
from . import views as rom_views, views_character as rom_views_character
from jgm import views_account as jgm_views_account
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', rom_views.home, name='rom_home'),

    url(r'^logout/$', jgm_views_account.logout, name='rom_logout'),
    url(r'^login/$', jgm_views_account.login, name='rom_login'),
    url('social-auth/', include('social_django.urls', namespace='social')),

    url(r'^character/create/$', rom_views_character.create, name='rom_character_create'),
    url(r'^character/(\d+)/$', rom_views_character.edit, name='rom_character_edit'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)