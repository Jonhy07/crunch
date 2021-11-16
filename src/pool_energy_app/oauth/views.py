from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponse
from django.urls import reverse

import os
from django.contrib.auth.mixins import LoginRequiredMixin

import urllib
import requests
import json
import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse

from pool_energy_app.forms.models import Network, SocialApplication, SocialApplicationPermission, Connector, StoreConnector, Store, Marketplace, MarketplaceConnector

from celery.decorators import task

# Create your views here.

def get_socialapplications(id):
	sa_dict = {};
	for sa in SocialApplication.objects.all():
		scope = [];
		separator = '';
		for sap in SocialApplicationPermission.objects.filter(social_application_id=sa.id):
			scope.append(sap.permission);
			separator = sap.separator;

		nn = Network.objects.get(id=sa.network_id);
		
		obj_sap = {
			'nombre':sa.name, 
			'url': sa.permissions_uri,	#urllib.parse.quote(sa.permissions_uri, safe=''),
			'logo':nn.logo, 
			'color':nn.color,
			'client_id': sa.application_key,
			'application_id': sa.application_id,
			'redirect_uri': (sa.callback_uri).strip(),	#urllib.parse.quote((sa.callback_uri).strip(), safe=''),
			'social_application': sa.id,
			'store': id
		};
		
		if len(scope) > 0:
			obj_sap.update({'scope': separator.join(scope)});
		
		sa_dict[sa.id] = obj_sap;
	return sa_dict;

def list_token(request):
	objects_list = []
	connectors = Connector.objects.filter(user_id=request.user.id)
	for conn in connectors:
		sa_dict = get_socialapplications()##obtener lista de social applications
		if conn.social_application_id in sa_dict:
			sa = sa_dict[conn.social_application_id]

			state = {"user": request.user.id, "social_application": conn.social_application_id, "name" : 0}
			url_params = {
				"client_id": sa['client_id'],
				"redirect_uri": sa['redirect_uri'],
				"scope": sa['scope'],
				"response_type":"code",
				"access_type":"offline",
				"prompt":"consent",
				"state": json.dumps(state, separators=(',', ':'))
			}

			url = '{}?{}'.format(sa['url'], urllib.parse.urlencode(url_params))
			
			dict_results = {
				'name': conn.name,
				'url': url,
				'logo': sa['logo'],
				'color': sa['color']
			}

			objects_list.append(dict_results);
	return render(request, "oauth/token/list.html",  context_data(request, {'objects_list': objects_list}))
	
def buttons_token(request, id):
	objects_list = []
	sa_dict = get_socialapplications(id)	##obtener diccionario de social applications
	for key in sa_dict:
		new_dict = sa_dict[key]
		new_dict.update({"user": request.user.id})
		objects_list.append(new_dict)
	return render(request, "oauth/token/buttons.html",  {'objects_list': objects_list, 'store_id': id})

def buttons_token_new(request, id):
	objects_list = []
	sa_dict = get_socialapplications(id);	##obtener diccionario de social applications
	for key in sa_dict:
		new_dict = sa_dict[key];
		new_dict.update({"user": request.user.id});
		objects_list.append(new_dict)
	return render(request, "account/firstConnector/connector.html",  {'objects_list': objects_list, 'store_id': id})

def marketplace_list_new(request, id):
	objects_list = []
	
	if request.method == 'POST':  # When the form is submitted
		todo = dict(request.POST)
		
		if 'connector_id' in todo and 'mktplc_list' in todo:
			for ele in todo['mktplc_list']:
				mkplc_conn = MarketplaceConnector()
				mkplc_conn.marketplace_id = ele
				mkplc_conn.connector_id = todo['connector_id'][0]
				mkplc_conn.save()
				
			msg = 'Se agregaron marketplaces exitosamente'
		else:
			msg = 'No seleccionó ningún marketplace. Conector agregado'
		
		forms = Store.objects.all()
		context = {
			'objects_list' : forms,
			'msg' : msg
		}
		
		return render(request, "forms/store/list.html", context)
	else:
		for mkplc in Marketplace.objects.all():
			chk_dict = {'id': mkplc.id, 'country': mkplc.country, 'mkplc_id': mkplc.marketplace_id, 'country_code':mkplc.country_code,'logo':mkplc.logo}
			objects_list.append(chk_dict)
	context = {
		'objects_list' : objects_list,
		'connector_id' : id
	}
	return render(request, "account/firstConnector/newMarketplace.html", context )

def accounts_token(request, id):
	objects_list = []
	sa_dict = get_socialapplications(id);	##obtener diccionario de social applications
	for key in sa_dict:
		new_dict = sa_dict[key];
		new_dict.update({"user": request.user.id});
		objects_list.append(new_dict)
	return render(request, "account/connector.html",  {'objects_list': objects_list, 'store_id': id})

def resp_token(request):
	final_url = ''
	clave = ''
	partner_id = ''
	if 'code' in request.GET:
		clave = 'code'
	elif 'spapi_oauth_code' in request.GET:
		clave = 'spapi_oauth_code'
		partner_id = request.GET.get('selling_partner_id');
	
	code = request.GET.get(clave)
	msg = ''
	
	if code:
		#state = json.loads(request.GET.get('state'));
		state = json.loads(request.GET.get('state').replace("&#34;", "\""));
		sap = SocialApplication.objects.get(id=state['social_application']);
		if sap:
			payload = {
				'client_id': sap.application_key,
				'redirect_uri': sap.callback_uri,
				'client_secret': sap.application_secret,
				'grant_type': 'authorization_code',
				'code': code
			};
			
			access_uri = sap.access_uri
			if 'myshopify' in access_uri:
				access_uri = access_uri.replace('{shop}', state['name'])
			
			#myheaders = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
			#response = requests.post(access_uri,params=payload)
			if clave == 'spapi_oauth_code' or sap.application_key.startswith("amzn1"):
				headersXXX = {'content-type': 'application/x-www-form-urlencoded',}
				response = requests.post(access_uri,data=payload,headers=headersXXX)	
			else:
				response = requests.post(access_uri,params=payload)	
	
			
			#Guardar la respuesta en Connector
			if response.status_code == 200:
				seconds_resp = 0
				if 'expires_in' in response.json():
					seconds_resp = int(response.json()['expires_in'])
				
				hr_actual = datetime.datetime.now();
				exp_hr = hr_actual + datetime.timedelta(seconds=int(seconds_resp));
				
				ref_token = ''
				if 'refresh_token' in response.json():
					ref_token = response.json()['refresh_token']
				
				acc_token = '';
				if 'refresh_token' in response.json():
					acc_token = response.json()['access_token']
				
				customer = 20210101
				if clave == 'spapi_oauth_code':
					customer = partner_id
				else:				
					if 'refresh_token' in response.json() and 'user_id' in response.json():
						customer = response.json()['user_id']
				
				dictDef = {
					'access_token':acc_token,
					'name':state['name'], 
					'refresh_token':ref_token, 
					'expiration_date':exp_hr, 
					'nonauto':True, 
					'social_application_id':state['social_application']
				}
				
				conn_id, created = Connector.objects.update_or_create(
					customer_id=customer,
					user_id=request.user.id,
					defaults=dictDef,
				)
				
				if created:
					print('Ya se guarda conector ' + str(conn_id.id))
				else:
					print('ya existe, actualizando conector '+ str(conn_id.id))
				
				store_obj = Store.objects.get(id=state['store'])
				
				store_connector = StoreConnector.objects.create(store=store_obj, connector=conn_id)
				store_connector.save()
				
				msg = 'Se agregó conector exitosamente'
				
				
			else:
				msg = 'ERROR al obtener access_token. Codigo ' + str(response.status_code)
				print("ERROR al obtener access_token. Codigo ", response.status_code);
	else:
		msg = 'ERROR ' + str(request.GET.get('error'))
	
	forms = Store.objects.all()
	context = {
		'objects_list' : forms,
		'msg' : msg
	}
	
	#return HttpResponseRedirect(reverse(final_url))
	#return redirect('/forms/store/list')
	#if msg == 'Se agregó conector exitosamente' and partner_id:
	if msg == 'Se agregó conector exitosamente' and store_connector.id and partner_id:
		url = reverse('oauth:marketplace_list', kwargs={'id': conn_id.id})
		return HttpResponseRedirect(url)
	else:
		return render(request, "store/list.html", context)

def marketplace_list(request, id):
	objects_list = []
	
	if request.method == 'POST':  # When the form is submitted
		todo = dict(request.POST)
		
		if 'connector_id' in todo and 'mktplc_list' in todo:
			for ele in todo['mktplc_list']:
				mkplc_conn = MarketplaceConnector()
				mkplc_conn.marketplace_id = ele
				mkplc_conn.connector_id = todo['connector_id'][0]
				mkplc_conn.save()
				
			msg = 'Se agregaron marketplaces exitosamente'
		else:
			msg = 'No seleccionó ningún marketplace. Conector agregado'
		
		forms = Store.objects.all()
		context = {
			'objects_list' : forms,
			'msg' : msg
		}
		
		return render(request, "store/list.html", context)
	else:
		for mkplc in Marketplace.objects.all():
			chk_dict = {'id': mkplc.id, 'country': mkplc.country, 'mkplc_id': mkplc.marketplace_id, 'country_code':mkplc.country_code}
			objects_list.append(chk_dict)
			
	context = {
		'objects_list' : objects_list,
		'connector_id' : id
	}
	
	return render(request, "oauth/token/marketplace_list.html", context )