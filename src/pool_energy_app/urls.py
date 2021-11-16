"""pool_energy_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import forms
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from pool_energy_app.charts.views import graphics, newdashboard, dashboard, newrow, deleteDashboard,deleteDashboardconfig, deleteRow

##########
from pool_energy_app.forms.views import create_network, list_network, update_network, delete_network
from pool_energy_app.forms.views import create_connector, list_connector, update_connector, delete_connector
from pool_energy_app.forms.views import create_social_application, list_social_application, update_social_application, delete_social_application

from pool_energy_app.forms.views import list_client, create_client, update_client, delete_client,newClient,send_invitation
from pool_energy_app.forms.views import list_store, create_store, update_store, delete_store,download_items
from pool_energy_app.forms.views import list_item, create_item, update_item, delete_item
from pool_energy_app.forms.views import list_liniostore, create_liniostore, update_liniostore, delete_liniostore
from pool_energy_app.forms.views import list_monthgoals, create_monthgoals, update_monthgoals, delete_monthgoals
from pool_energy_app.forms.views import list_action, create_action, update_action, delete_action
from pool_energy_app.forms.views import list_itemaction, create_itemaction, update_itemaction, delete_itemaction
from pool_energy_app.forms.views import list_userstore, create_userstore, update_userstore, delete_userstore
from pool_energy_app.forms.views import list_homologation,create_homologation, update_homologation, delete_homologation,itemsStore,itemsS2,itemsStoreAction

#aouth
from pool_energy_app.oauth.views import buttons_token, resp_token, list_token, marketplace_list,accounts_token,buttons_token_new,marketplace_list_new

##########

from pool_energy_app.graphs.views import newgraph, addgraph, deletegraph, pie, update_pie, bar, update_bar, legend, create_bar_legend, namebar, add_yrow, create_bar_name, card, update_card, tab, update_tab, nametab, add_col, create_tab_name, legendtab, add_col_legend, filterlegendbar, filtercampo, create_filter, filter_finsh, filterlegendpie, filterlegendcard
from pool_energy_app.common.views import expired
from pool_energy_app.config.views import users, usereditindex, update_user, list_dashboards


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', list_store, name='home'),

	#############################################
	################### FORMS ###################
	#############################################
#---------------------------------------------------------------------network---------------------------------------------------------------------#
    #path('forms/list_network', list_network, name='list_network'),
	#url(r'^network.list/', list_network, name='list'),#---
	#url(r'^network.(?P<id>\d+)/change/', update_network, name='update'),#---
	#url(r'^network.(?P<id>\d+)/delete/', delete_network, name='delete'),#---

#--------------------------------------------------------------------social app---------------------------------------------------------------------#
	path('forms/list_social_application', list_social_application, name='list_social_application'),
	path('forms/create_social_application', create_social_application, name='create_social_application'),
	url(r'forms/socialapplication/(?P<id>\d+)/change/', update_social_application, name='update_social_application'),
	url(r'forms/socialapplication/(?P<id>\d+)/delete/', delete_social_application, name='delete_social_application'),

	url(r'forms/invitation', send_invitation, name='send_invitation'),

	########################
	########################

	path('forms/newClient/', newClient, name='newClient'),#-- listo
	url(r'forms/token/(?P<id>\d+)/buttons/', buttons_token_new, name='buttons_token_new'),#-- listo
	url(r'token/resp/', resp_token, name='resp_token'),#-- por arreglar
	url(r'token/list/', list_token, name='list_token'),#-- por arreglar
	url(r'forms/marketplace/(?P<id>\d+)/', marketplace_list_new, name='marketplace_list_new'),#--listo

	########################
	########################
#---------------------------------------------------------------------connector---------------------------------------------------------------------#
	#url(r'^connector.add/', create_connector, name='create'),#--
	#url(r'^connector.list/', list_connector, name='list'),#--
	#url(r'^connector.(?P<id>\d+)/change/', update_connector, name='update'),#--
	#url(r'^connector.(?P<id>\d+)/delete/', delete_connector, name='delete'),#--

#---------------------------------------------------------------------Customer----------------------------------------------------------------------#
	path('forms/list_client', list_client, name='list_client'),
	path('forms/create_client', create_client, name='create_client'),
	url(r'forms/client/(?P<id>\d+)/change/', update_client, name='update_client'),
	url(r'forms/client/(?P<id>\d+)/delete/', delete_client, name='delete_client'),

#-----------------------------------------------------------------------Store-----------------------------------------------------------------------#
	path('forms/list_store', list_store, name='list_store'),
	path('forms/create_store', create_store, name='create_store'),
	url(r'forms/store/(?P<id>\d+)/change/', update_store, name='update_store'),
	url(r'forms/store/(?P<id>\d+)/delete/', delete_store, name='delete_store'),
	url(r'forms/store/(?P<id>\d+)/download/', download_items, name='download'),

#-----------------------------------------------------------------------Item------------------------------------------------------------------------#
	path('forms/list_item', list_item, name='list_item'),
	path('forms/create_item', create_item, name='create_item'),
	url(r'forms/item/(?P<id>\d+)/change/', update_item, name='update_item'),
	url(r'forms/item/(?P<id>\d+)/delete/', delete_item, name='delete_item'),
#-----------------------------------------------------------------------LinioStore------------------------------------------------------------------------#
	#url(r'^liniostore.(?P<id>\d+)/list/', list_liniostore, name='list'),#--
	#url(r'^liniostore.(?P<id>\d+)/add/', create_liniostore, name='create'),#--
	#url(r'^liniostore.(?P<id>\d+)/change/', update_liniostore, name='update'),#--
	#url(r'^liniostore.(?P<id>\d+)/delete/', delete_liniostore, name='delete'),#--
#-----------------------------------------------------------------------MonthGoals------------------------------------------------------------------------#
	path('forms/list_monthgoals', list_monthgoals, name='list_monthgoals'),
	path('forms/create_monthgoals', create_monthgoals, name='create_monthgoals'),
	url(r'forms/monthgoals/(?P<id>\d+)/change/', update_monthgoals, name='update_monthgoals'),
	url(r'forms/monthgoals/(?P<id>\d+)/delete/', delete_monthgoals, name='delete_monthgoals'),
#-----------------------------------------------------------------------Action------------------------------------------------------------------------#
	path('forms/list_action', list_action, name='list_action'),
	path('forms/create_action', create_action, name='create_action'),
	url(r'forms/action/(?P<id>\d+)/change/', update_action, name='update_action'),
	url(r'forms/action/(?P<id>\d+)/delete/', delete_action, name='delete_action'),
#-----------------------------------------------------------------------ItemAction------------------------------------------------------------------------#
	path('forms/list_itemaction', list_itemaction, name='list_itemaction'),
	path('forms/create_itemaction', create_itemaction, name='create_itemaction'),#--
	url(r'forms/itemaction/(?P<id>\d+)/change/', update_itemaction, name='update_itemaction'),#--
	url(r'forms/itemaction/(?P<id>\d+)/delete/', delete_itemaction, name='delete_itemaction'),#--
	path('forms/itemaction/cargarStore/', itemsStoreAction, name='cargarStoreAction'),#--

#-----------------------------------------------------------------------UserStore------------------------------------------------------------------------#
	path('forms/list_userstore', list_userstore, name='list_userstore'),
	path('forms/create_userstore', create_userstore, name='create_userstore'),
	url(r'forms/userstore/(?P<id>\d+)/change/', update_userstore, name='update_userstore'),
	url(r'forms/userstore/(?P<id>\d+)/delete/', delete_userstore, name='delete_userstore'),
#-----------------------------------------------------------------------Homologation------------------------------------------------------------------------#
	path('forms/list_homologation', list_homologation, name='list_homologation'),
	path('forms/create_homologation', create_homologation, name='create_homologation'),#--
	url(r'forms/homologation/(?P<id>\d+)/change/', update_homologation, name='update_homologation'),#--
	url(r'forms/homologation/(?P<id>\d+)/delete/', delete_homologation, name='delete_homologation'),#--
	#url(r'^homologation/cargarStore/', itemsStore, name='cargarStore'),
	#url(r'^homologation/cargar2/',itemsS2, name='cargarS'),

	#############################################
	################### AOUTH ###################
	#############################################

	url(r'oauth/token/(?P<id>\d+)/buttons/', buttons_token, name='buttons_token'),
	url(r'oauth/token/resp/', resp_token, name='resp_token'),#--
	url(r'token/list/', list_token, name='list_token'),#--
	url(r'marketplace/view/(?P<id>\d+)/', marketplace_list, name='marketplace_list'),#--

	#############################################
	#############################################
	#############################################

    #Usuarios
    path('config/list_users', users, name='list_users'),
    path('config/users', usereditindex, name='config_user'),
    path('config/updateuser', update_user, name='config_update_user'),

    #Dashboards
    path('config/list_dashboards', list_dashboards, name='list_dashboards'),
    path('config/dashboard/<int:id>/delete', deleteDashboardconfig,name='confi_dashboard_delete'),

    #------------Control----------
    path('expired/', expired, name='expired'),

    #------------Charts-----------
    path('dashboard/add', newdashboard, name='dashboard_add'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/add/row', newrow, name='dashboard_add_row'),
    path('dashboard/<int:id>/delete/', deleteDashboard,name='delete_dashboard'),
    path('dashboard/row/<int:id>/delete/', deleteRow,name='delete_row'),

    #------------Grpahs-------------
    path('dashboard/row/graph/<int:id>/new', newgraph,name='new_graph'),
    path('dashboard/row/graph/add', addgraph,name='add_graph'),
    path('dashboard/row/graph/<int:id>/delete', deletegraph,name='delete_graph'),

    #------------Type_Grpahs-------------
    #Pie
    path('dashboard/row/graph/add/<int:id>/pie', pie,name='pie'),
    path('dashboard/row/graph/update/pie', update_pie,name='update_graph_pie'),

    #Bar
    path('dashboard/row/graph/add/<int:id>/bar', bar,name='bar'),
    path('dashboard/row/graph/update/bar', update_bar,name='update_graph_bar'),
    path('dashboard/row/graph/add/<int:id>/bar/legend', legend,name='legend_bar'),
    path('dashboard/row/graph/create/bar/legend', create_bar_legend,name='create_bar_legend'),

    #Bar name
    path('dashboard/row/graph/add/<int:id>/bar/name', namebar,name='name_bar'),
    path('dashboard/row/graph/create/bar/name', add_yrow,name='add_yrow'),
    path('dashboard/row/graph/create/bar/finish', create_bar_name,name='create_bar_name'),

    #Card
    path('dashboard/row/graph/add/<int:id>/card', card,name='card'),
    path('dashboard/row/graph/update/card', update_card,name='update_graph_card'),

    #Tab
    path('dashboard/row/graph/add/<int:id>/tab', tab,name='tab'),
    path('dashboard/row/graph/update/tab', update_tab,name='update_graph_tab'),
    path('dashboard/row/graph/add/<int:id>/tab/legend', legendtab,name='legend_tab'),
    path('dashboard/row/graph/create/tab/legend', add_col_legend,name='add_col_legend'),

    #Tab name
    path('dashboard/row/graph/add/<int:id>/tab/name', nametab,name='name_tab'),
    path('dashboard/row/graph/create/tab/name', add_col,name='add_col'),
    path('dashboard/row/graph/create/tab/finish', create_tab_name,name='create_tab_name'),

    #Filtros bar, tab
    path('dashboard/row/graph/add/<int:id>/filter/bar', filterlegendbar,name='filter_legend_bar'),

    #Filtros pie
    path('dashboard/row/graph/add/<int:id>/filter/pie', filterlegendpie,name='filter_legend_pie'),

    #Filtros pie
    path('dashboard/row/graph/add/<int:id>/filter/card', filterlegendcard,name='filter_legend_card'),

    #filtros general
    path('dashboard/row/graph/create/filter', create_filter,name='create_filter'),
    path('dashboard/row/graph/create/filter/finish', filter_finsh,name='filter_finsh'),

    #AJAX
    path('dashboard/row/graph/filter/campo/<str:id_graph>/<str:id_filtro>', filtercampo,name='filter_campo'),
]