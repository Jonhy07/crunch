from django.conf.urls import url
from django.contrib import admin

from .views import buttons_token, resp_token, list_token, marketplace_list

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	#url(r'^token.buttons/', buttons_token, name='buttons'),
	url(r'^token.(?P<id>\d+)/buttons/', buttons_token, name='buttons'),
	url(r'^token.resp/', resp_token, name='resp'),
	url(r'^token.list/', list_token, name='list'),
	url(r'^marketplace/view/(?P<id>\d+)/', marketplace_list, name='marketplace_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)