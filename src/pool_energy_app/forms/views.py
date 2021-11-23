import os
import pyarrow
import xlsxwriter
import pandas as pd
from io import BytesIO

from .filters import ItemFilter
from django.conf.urls import url
from django.core import paginator
from pool_energy_app.forms import filters
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import FilteredRelation, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponseRedirect

from .models import Item, Marketplace
from .models import User
from .models import Store
from .models import Action
from .models import Client
from .models import Network
from .models import Connector
from .models import UserStore
from .models import MonthGoals
from .models import LinioStore
from .models import ItemAction
from .models import Homologation
from .models import SocialApplication

from .form import ItemModelForm
from .form import StoreModelForm
from .form import ActionModelForm
from .form import ClientModelForm
from .form import ClientNew
from .form import ClientSendMail
from .form import NetworkModelForm
from .form import ConnectorModelForm
from .form import UserStoreModelForm
from .form import ItemActionModelForm
from .form import LinioStoreModelForm
from .form import MonthGoalsModelForm
from .form import HomologationModelForm
from .form import SocialApplicationModelForm

#from codigo import display_table_objs
#---------------------------------------------------------------------Network---------------------------------------------------------------------#

def create_network(request):
	form = NetworkModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return redirect('/forms/network/list')

	context = {
		'form' : form
	}
	return render(request, "network/add.html",  context)

def list_network(request):
	forms = Network.objects.all()
	context = {
		'objects_list' : forms,
	}
	return render(request, "forms/network/list.html", context)

def update_network(request, id):
	unique_name = get_object_or_404(Network, id=id)
	form = NetworkModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return redirect('/forms/network/list')

	context = {
		'form' : form
	}
	return render(request, "network/add.html", context)

def delete_network(request, id):
	item_to_delete = Network.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return redirect('/forms/network/list')

#---------------------------------------------------------------------SocialApplication---------------------------------------------------------------------#
def send_mail(mail,request):
	usuario = get_object_or_404(User, id=request.user.id)
	context = {'mail':mail,'username':'jefe','current_site':{'name':'nombre'},'user':usuario}
	template=get_template('account/email/invitation_message.html')
	content = template.render(context)
	email = EmailMultiAlternatives('¡El DNA te está esperando!','',settings.EMAIL_HOST_USER,[mail])
	email.attach_alternative(content,'text/html')
	email.send()

def send_invitation(request):
	form = ClientSendMail(request.POST or None, request.FILES or None)
	if form.is_valid():
		send_mail(form.cleaned_data['email'],request)
		return HttpResponseRedirect("/forms/list_store")
	context = {
		'form' : form
		,'Text':'Invitar'
	}
	return render(request, "forms/application/add.html", context)

def list_social_application(request):
	forms = SocialApplication.objects.all()
	context = {
		'objects_list' : forms
	}
	return render(request, "forms/application/list.html", context)

def create_social_application(request):
	form = SocialApplicationModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_social_application")
	context = {
		'form' : form
		,'Text':'Crear'
	}
	return render(request, "forms/application/add.html", context)

def update_social_application(request, id):
	unique_name = get_object_or_404(SocialApplication, id=id)
	form = SocialApplicationModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_social_application")
	context = {
		'form' : form
		,'Text':'Actualizar'
	}
	return render(request, "forms/application/add.html", context)

def delete_social_application(request, id):
	item_to_delete = SocialApplication.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_social_application")

#----------------------------------connector------------------------------------------

def create_connector(request):
	form = ConnectorModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return redirect('/forms/connector/list')
	context = {
		'form' : form
	}
	return render(request, "connector/add.html")

def list_connector(request):
	forms = Connector.objects.all()
	context = {
		'objects_list' : forms
	}
	return render(request, "forms/connector/list.html")

def update_connector(request, id):
	unique_name = get_object_or_404(Connector, id=id)
	form = ConnectorModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return redirect('/forms/connector/list')

	context = {
		'form' : form
	}
	return render(request, "connector/add.html")

def delete_connector(request, id):
	item_to_delete = Connector.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return redirect('/forms/connector/list')

def social_connect(request):
	context = {}
	return render(request, "connector/social_connect.html",  context_data(request,context))

#----------------------------------Customer-------------------------------------------

def list_client(request):
	forms = Client.objects.all()
	context = {
		'objects_list' : forms
	}
	return render(request, "forms/client/list.html", context)

def create_client(request):
	form = ClientModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_client")
	context = {
		'form' : form
		,'Text':'Crear'
	}
	return render(request, "forms/client/add.html", context)

def update_client(request, id):
	unique_name = get_object_or_404(Client, id=id)
	form = ClientModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_client")
	context = {
		'form' : form
		,'Text':'Actualizar'
	}
	return render(request, "forms/client/add.html", context)

def delete_client(request, id):
	item_to_delete = Client.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_client")

def download_items(request, id):
    deStore=Item.objects.filter(store_id=id)
    deStoreName=Store.objects.filter(id=id)
    qset = deStore.values('marketplace','ktp','sku','nombre')
    qsetName = deStoreName.values('name')
    dfName = pd.DataFrame(list(qsetName))
    nombreStore=str(dfName.iloc[0,0])
    dfProductos = pd.DataFrame(list(qset))
    dfProductos.insert(0, 'Tienda',nombreStore)
    dfProductos.reset_index(drop=True,inplace=True)
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        dfProductos.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        filename = 'inventario'
        content_type = 'application/vnd.ms-excel'
        response = HttpResponse(b.getvalue(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
        return response
#----------------------------------Store-------------------------------------------

def list_store(request):
	current_user = request.user
	if current_user.is_authenticated:
		stores = UserStore.objects.filter(user=current_user.id).values_list('store',flat=True)
		forms = Store.objects.filter(pk__in=[stores])
	else:
		forms = Store.objects.all()
	context = {
		'objects_list' : forms
	}
	return render(request, "forms/store/list.html", context)

def create_store(request):
	form = StoreModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_store")
	context = {
		'form' : form
		,'Text':'Crear'
	}
	return render(request, "forms/store/add.html", context)

def newClient(request):
	form = ClientNew(request.POST or None, request.FILES or None)
	if form.is_valid():
		idClient=form.save().id
		cliente = get_object_or_404(Client, id=idClient)
		elStore=Store(name=cliente.owner_name,client_id=cliente.id,status='Activado',blueprint='Link')
		elStore.save()
		clientStore= UserStore(store_id=elStore.id,user_id=request.user.id)
		clientStore.save()
		return HttpResponseRedirect("/forms/token/{}/buttons".format(elStore.id))
	context = {
		'form' : form
		,'Text':'Crear'
	}
	return render(request, "account/firstConnector/newClient.html", context)

def update_store(request, id):
	unique_name = get_object_or_404(Store, id=id)
	form = StoreModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_store")
	context = {
		'form' : form
		,'Text':'Actualizar'
	}
	return render(request, "forms/store/add.html", context)

def delete_store(request, id):
	item_to_delete = Store.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_store")

#-----------------------------------Item-------------------------------------------

def list_item(request):
	if "GET" == request.method:
		forms = Item.objects.all()
		nPagina=1
		filtroItems= ItemFilter(request.GET,queryset=forms)
		storeId=0
		ktp=''
		if 'store' in request.GET :
			storeId=request.GET['store']
			if storeId != 0:
				forms = filtroItems.qs
		if 'ktp' in request.GET :
			ktp=request.GET['ktp']
		paginacion=Paginator(forms,10)
		pagina1=paginacion.page(1)
		if 'page' in request.GET :
			nPagina=int(request.GET['page'])
		if int(nPagina) >= int(paginacion.num_pages):
			nPagina=1
		pagina1=paginacion.page(nPagina)
		context = {
			'objects_list' : pagina1,
			'Filtro':filtroItems,
			'storeId':storeId,
			'ktp':ktp
		}
		return render(request, "forms/item/list.html", context)
	else:
		excel_file = request.FILES["excel_file"]
		df = pd.read_excel(excel_file,converters={'ktp':str})
		if 'Marketplace' in df.columns:
			df['Marketplace'].fillna(-1,inplace=True)
		if 'marketplace' in df.columns:
			df['marketplace'].fillna(-1,inplace=True)
		numero=0
		for i in range(df.shape[0]):
			if (df.iloc[i][1]==-1):
				numero=i
				break
			elif (i==df.shape[0]-1):
				numero=i+1
		df=df.iloc[:numero,:]
		for i in range(df.shape[0]):
			flag=1
			try:
				store=Store.objects.get(name=df.iloc[i][0])
			except Exception as e:
				flag=0
			try:
				deStore=Item.objects.filter(store_id=store.id,marketplace=df.iloc[i][1])
				contador=0
				item={}
				for j in deStore:
					if (j.ktp == df.iloc[i][2]):
						contador+=1
						item=j
				if (contador > 1):
					flag=0
				else:
					item.costo=float(df.iloc[i][5])

			except Exception as e:
				flag=0

			if flag:
				item.save()
		forms = Item.objects.all()
		nPagina=1
		filtroItems= ItemFilter(request.GET,queryset=forms)
		storeId=0
		ktp=''
		if 'store' in request.GET :
			storeId=request.GET['store']
			if storeId != 0:
				forms = filtroItems.qs
		if 'ktp' in request.GET :
			ktp=request.GET['ktp']
		paginacion=Paginator(forms,10)
		pagina1=paginacion.page(1)
		if 'page' in request.GET :
			nPagina=int(request.GET['page'])
		if int(nPagina) >= int(paginacion.num_pages):
			nPagina=1
		pagina1=paginacion.page(nPagina)
		context = {
			'objects_list' : pagina1,
			'Filtro':filtroItems,
			'storeId':storeId,
			'ktp':ktp
		}
		return render(request, "forms/item/list.html", context)

def create_item(request):
	form = ItemModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_item")
	context = {
		'form' : form
		,'Text':'Crear'
	}
	return render(request, "forms/item/add.html", context)

def update_item(request, id):
	unique_name = get_object_or_404(Item, id=id)
	form = ItemModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_item")
	context = {
		'form' : form
		,'Text':'Actualizar'
	}
	return render(request, "forms/item/add.html", context)

def delete_item(request, id):
	item_to_delete = Item.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_item")

#---------------------------------LinioStore-----------------------------------------

def list_liniostore(request, id):
	#SocialApplicationPermission.objects.filter(social_application_id=sa.id):
	forms = LinioStore.objects.filter(store_id=id)
	context = {
		'objects_list' : forms,
		'store_id' : id
	}
	return render(request, "forms/liniostore/list.html", context)

def create_liniostore(request, id):
	form = LinioStoreModelForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		form.save()
		return redirect('/forms/liniostore/' + str(form.instance.store_id) +'/list')

	form.fields['store'].queryset = Store.objects.filter(id=id)
	
	context = {
		'form' : form
	}
	return render(request, "liniostore/add.html", context)

def update_liniostore(request, id):
	unique_name = get_object_or_404(LinioStore, id=id)
	form = LinioStoreModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return redirect('/forms/liniostore/list')

	context = {
		'form' : form
	}
	return render(request, "liniostore/add.html", context)

def delete_liniostore(request, id):
	item_to_delete = LinioStore.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return redirect('/forms/liniostore/list')

#-----------------------------------MonthGoals-------------------------------------------

def list_monthgoals(request):
	if "GET" == request.method:
		forms = MonthGoals.objects.all()
		context = {
			'objects_list' : forms
		}
		return render(request, "forms/monthgoals/list.html", context)
	else:
		excel_file = request.FILES["excel_file"]
		df = pd.read_excel(excel_file,converters={'ktp':str})
		try:
			for i in range(df.shape[0]):
				flag=1
				#store
				try:
					store=Store.objects.get(name=df.iloc[i,0])
				except Exception as e:
					flag=0
				#mes
				mesString=df.iloc[i,1].lower()
				if mesString=="enero":
					mes=1
				elif mesString=="febrero":
					mes=2
				elif mesString=="marzo":
					mes=3
				elif mesString=="abril":
					mes=4
				elif mesString=="mayo":
					mes=5
				elif mesString=="junio":
					mes=6
				elif mesString=="julio":
					mes=7
				elif mesString=="agosto":
					mes=8
				elif mesString=="septiembre":
					mes=9
				elif mesString=="octubre":
					mes=10
				elif mesString=="noviembre":
					mes=11
				elif mesString=="diciembre":
					mes=12
				else:
					flag=0
				if flag:
					MonthGoals.objects.create(store=store, mes=mes, anio=df.iloc[i,2], fee=df.iloc[i,3],sales_goal=df.iloc[i,4],units_goal=df.iloc[i,5],ads_spend_limit=df.iloc[i,6])
		except Exception as e:
			print(e)
		forms = MonthGoals.objects.all()
		context = {
			'objects_list' : forms
		}
		return render(request, "forms/monthgoals/list.html", context)

def create_monthgoals(request):
	form = MonthGoalsModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_monthgoals")
	context = {
		'form' : form
		,'Text' : 'Crear'
	}
	return render(request, "forms/monthgoals/add.html", context)

def update_monthgoals(request, id):
	unique_name = get_object_or_404(MonthGoals, id=id)
	form = MonthGoalsModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_monthgoals")
	context = {
		'form' : form
		,'Text' : 'Actualizar'
	}
	return render(request, "forms/monthgoals/add.html", context)

def delete_monthgoals(request, id):
	item_to_delete = MonthGoals.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_monthgoals")

#-----------------------------------Action-------------------------------------------

def list_action(request):
	forms = Action.objects.all()
	context = {
		'objects_list' : forms
	}
	return render(request, "forms/action/list.html", context)

def create_action(request):
	form = ActionModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_action")
	context = {
		'form' : form
		,'Text' : 'Crear'
	}
	return render(request, "forms/action/add.html", context)

def update_action(request, id):
	unique_name = get_object_or_404(Action, id=id)
	form = ActionModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_action")
	context = {
		'form' : form
		,'Text' : 'Actualizar'
	}
	return render(request, "forms/action/add.html", context)

def delete_action(request, id):
	item_to_delete = Action.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_action")

#-----------------------------------ItemAction-------------------------------------------

def list_itemaction(request):
	if "GET" == request.method:
		forms = ItemAction.objects.all()
		context = {
			'objects_list' : forms
		}
		return render(request, "forms/itemaction/list.html", context)
	else:
		excel_file = request.FILES["excel_file"]
		df = pd.read_excel(excel_file,converters={'ktp':str})
		for i in range(df.shape[0]):
			flag=1
			try:
				store=Store.objects.get(name=df.iloc[i][0])
			except Exception as e:
				flag=0
			try:
				item = Item.objects.get(marketplace=df.iloc[i][1],ktp=df.iloc[i][2],sku = df.iloc[i][3])
			except Exception as e:
				flag=0
			try:
				action = Action.objects.get(name = df.iloc[i][5])
			except Exception as e:
				flag=0
			if flag:
				ItemAction.objects.create(store=store,sku=item.sku,ktp=item.ktp ,item=item, action=action, comment=df.iloc[i][6])

		forms = ItemAction.objects.all()
		context = {
			'objects_list' : forms
		}
		return render(request, "forms/itemaction/list.html", context)

def create_itemaction(request):
	form = ItemActionModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_itemaction")
	context = {
		'form' : form
		,'Text' : 'Crear'
	}
	return render(request, "forms/itemaction/add.html", context)

def itemsStoreAction(request):
	store_id = request.GET.get('store_id')
	items = Item.objects.filter(store_id=store_id).all()
	return render(request, 'forms/itemaction/drop.html', {'items': items})

def update_itemaction(request, id):
	unique_name = get_object_or_404(ItemAction, id=id)
	form = ItemActionModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_itemaction")
	context = {
		'form' : form
		,'Text' : 'Actualizar'
	}
	return render(request, "forms/itemaction/add.html", context)

def delete_itemaction(request, id):
	item_to_delete = ItemAction.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_itemaction")

#-----------------------------------UserStore-------------------------------------------

def list_userstore(request):
	forms = UserStore.objects.all()
	context = {
		'objects_list' : forms
	}
	return render(request, "forms/userstore/list.html", context)

def create_userstore(request):
	form = UserStoreModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_userstore")
	context = {
		'form' : form
		,'Text' : 'Crear'
	}
	return render(request, "forms/userstore/add.html", context)

def update_userstore(request, id):
	unique_name = get_object_or_404(UserStore, id=id)
	form = UserStoreModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_userstore")
	context = {
		'form' : form
		,'Text' : 'Actualizar'
	}
	return render(request, "forms/userstore/add.html", context)

def delete_userstore(request, id):
	item_to_delete = UserStore.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_userstore")

#----------------------------------- Homologation -------------------------------------------

def list_homologation(request):
	forms = Homologation.objects.all()
	context = {
		'objects_list' : forms
	}
	return render(request, "forms/homologation/list.html", context)

def itemsStore(request):
	store_id = request.GET.get('store_id')
	items = Item.objects.filter(store_id=store_id).all()
	return render(request, 'forms/homologation/drop.html', {'items': items})

def itemsS2(request):
	store_id = request.GET.get('store_id')
	items = Item.objects.filter(store_id=store_id).all()
	return render(request, 'forms/homologation/drop.html', {'items': items})

def create_homologation(request):
	form = HomologationModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_homologation")
	context = {
		'form' : form
		,'Text' : 'Crear'
	}
	return render(request, "forms/homologation/add.html", context)

def update_homologation(request, id):
	unique_name = get_object_or_404(Homologation, id=id)
	form = HomologationModelForm(request.POST or None, request.FILES or None, instance=unique_name)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/forms/list_homologation")
	context = {
		'form' : form
		,'Text' : 'Actualizar'
	}
	return render(request, "forms/homologation/add.html", context)

def delete_homologation(request, id):
	item_to_delete = Homologation.objects.filter(pk=id)
	if item_to_delete.exists():
		item_to_delete[0].delete()
	return HttpResponseRedirect("/forms/list_homologation")