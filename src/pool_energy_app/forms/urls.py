from django.conf.urls import url
from django.urls import path
from django.contrib import admin

from .views import create_network, list_network, update_network, delete_network
from .views import create_connector, list_connector, update_connector, delete_connector
from .views import create_social_application, list_social_application, update_social_application, delete_social_application

from .views import list_client, create_client, update_client, delete_client
from .views import list_store, create_store, update_store, delete_store,download_items
from .views import list_item, create_item, update_item, delete_item
from .views import list_liniostore, create_liniostore, update_liniostore, delete_liniostore
from .views import list_monthgoals, create_monthgoals, update_monthgoals, delete_monthgoals
from .views import list_action, create_action, update_action, delete_action
from .views import list_itemaction, create_itemaction, update_itemaction, delete_itemaction
from .views import list_userstore, create_userstore, update_userstore, delete_userstore
from .views import list_homologation,create_homologation, update_homologation, delete_homologation,itemsStore,itemsS2,itemsStoreAction

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#---------------------------------------------------------------------network---------------------------------------------------------------------#
	url(r'^network.add/', create_network, name='create'),
	url(r'^network.list/', list_network, name='list'),
	url(r'^network.(?P<id>\d+)/change/', update_network, name='update'),
	url(r'^network.(?P<id>\d+)/delete/', delete_network, name='delete'),

#--------------------------------------------------------------------social app---------------------------------------------------------------------#
	url(r'^socialapplication.add/', create_social_application, name='create'),
	url(r'^socialapplication.list/', list_social_application, name='list'),
	url(r'^socialapplication.(?P<id>\d+)/change/', update_social_application, name='update'),
	url(r'^socialapplication.(?P<id>\d+)/delete/', delete_social_application, name='delete'),

#---------------------------------------------------------------------connector---------------------------------------------------------------------#
	url(r'^connector.add/', create_connector, name='create'),
	url(r'^connector.list/', list_connector, name='list'),
	url(r'^connector.(?P<id>\d+)/change/', update_connector, name='update'),
	url(r'^connector.(?P<id>\d+)/delete/', delete_connector, name='delete'),

#---------------------------------------------------------------------Customer----------------------------------------------------------------------#
	url(r'^client.list/', list_client, name='client_list'),
	url(r'^client.add/', create_client, name='create'),
	url(r'^client.(?P<id>\d+)/change/', update_client, name='update'),
	url(r'^client.(?P<id>\d+)/delete/', delete_client, name='delete'),

#-----------------------------------------------------------------------Store-----------------------------------------------------------------------#
	url(r'^store.list/', list_store, name='list'),
	url(r'^store.add/', create_store, name='create'),
	url(r'^store.(?P<id>\d+)/change/', update_store, name='update'),
	url(r'^store.(?P<id>\d+)/delete/', delete_store, name='delete'),
	url(r'^store.(?P<id>\d+)/download/', download_items, name='download'),

#-----------------------------------------------------------------------Item------------------------------------------------------------------------#
	url(r'^item.list/', list_item, name='list'),
	url(r'^item.add/', create_item, name='create'),
	url(r'^item.(?P<id>\d+)/change/', update_item, name='update'),
	url(r'^item.(?P<id>\d+)/delete/', delete_item, name='delete'),
#-----------------------------------------------------------------------LinioStore------------------------------------------------------------------------#
	#url(r'^liniostore.list/', list_liniostore, name='list'),
	url(r'^liniostore.(?P<id>\d+)/list/', list_liniostore, name='list'),
	url(r'^liniostore.(?P<id>\d+)/add/', create_liniostore, name='create'),
	url(r'^liniostore.(?P<id>\d+)/change/', update_liniostore, name='update'),
	url(r'^liniostore.(?P<id>\d+)/delete/', delete_liniostore, name='delete'),
#-----------------------------------------------------------------------MonthGoals------------------------------------------------------------------------#
	url(r'^monthgoals.list/', list_monthgoals, name='list'),
	url(r'^monthgoals.add/', create_monthgoals, name='create'),
	url(r'^monthgoals.(?P<id>\d+)/change/', update_monthgoals, name='update'),
	url(r'^monthgoals.(?P<id>\d+)/delete/', delete_monthgoals, name='delete'),
#-----------------------------------------------------------------------Action------------------------------------------------------------------------#
	url(r'^action.list/', list_action, name='list'),
	url(r'^action.add/', create_action, name='create'),
	url(r'^action.(?P<id>\d+)/change/', update_action, name='update'),
	url(r'^action.(?P<id>\d+)/delete/', delete_action, name='delete'),
#-----------------------------------------------------------------------ItemAction------------------------------------------------------------------------#
	url(r'^itemaction.list/', list_itemaction, name='list'),
	url(r'^itemaction.add/', create_itemaction, name='create'),
	url(r'^itemaction.(?P<id>\d+)/change/', update_itemaction, name='update'),
	url(r'^itemaction.(?P<id>\d+)/delete/', delete_itemaction, name='delete'),
	url(r'^itemaction/cargarStore/', itemsStoreAction, name='cargarStoreAction'),
#		url(r'^excel/', excel, name='excel'),	
#-----------------------------------------------------------------------UserStore------------------------------------------------------------------------#
	url(r'^userstore.list/', list_userstore, name='list'),
	url(r'^userstore.add/', create_userstore, name='create'),
	url(r'^userstore.(?P<id>\d+)/change/', update_userstore, name='update'),
	url(r'^userstore.(?P<id>\d+)/delete/', delete_userstore, name='delete'),
#-----------------------------------------------------------------------UserStore------------------------------------------------------------------------#
	url(r'^homologation.list/', list_homologation, name='list'),
	url(r'^homologation.add/', create_homologation, name='create'),
	url(r'^homologation.(?P<id>\d+)/change/', update_homologation, name='update'),
	url(r'^homologation.(?P<id>\d+)/delete/', delete_homologation, name='delete'),
	url(r'^homologation/cargarStore/', itemsStore, name='cargarStore'),
	url(r'^homologation/cargar2/',itemsS2, name='cargarS'),

	# path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)