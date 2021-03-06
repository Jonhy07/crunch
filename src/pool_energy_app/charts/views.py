import os
import requests
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import json
from django.contrib import messages
from requests.api import options
from pool_energy_app.charts.forms import DashboardForm, RowForm
from django.shortcuts import render, redirect, get_object_or_404

from pool_energy_app.users.models import Rol
from pool_energy_app.forms.models import Marketplace, UserStore,Store,MarketplaceConnector,StoreConnector
from .models import Dashboard, Row, User_Dashboard
import json
from datetime import date, timedelta
import calendar

def obtener_filtros_tienda(store_str,min,max):
    laStore = list(Store.objects.filter(name=store_str).values_list('id',flat=True))[0]
    marketplaces=[]
    plataformas=[]

    API_V2_STR = os.environ.get('API_V2_STR')
    _txt='"store":"{}","fecha_min":"{}","fecha_max":"{}"'.format(laStore,min.replace('-',''),max.replace('-',''))
    _txt= '{' + _txt + '}'
    _json=json.loads(_txt)
    token=""
    _headers={'Content-Type':'application/json', 'Autorization':token}
    response=requests.post(API_V2_STR+'agrupacion_por_tienda', data=json.dumps(_json), headers=_headers)
    plataformas=response.json()['plataformas']
    marketplaces=response.json()['marketplace']
    mplaces=[]
    for m in marketplaces:
        if m != 'Sin Marketplace':
            m_i= Marketplace.objects.filter(marketplace_id=m).values_list('country',flat=True)[0]
            mplaces.append(m_i)
        else:
            mplaces.append('Sin Marketplace')

    if len(plataformas)==0:
        plataformas.insert(0,'No Aplica')
        indice_plataforma='No Aplica'
    elif len(plataformas)==1:
        indice_plataforma=plataformas[0]
    else:
        indice_plataforma='No Seleccionado'
        plataformas.insert(0,'No Seleccionado')

    if len(mplaces)==0:
        mplaces.insert(0,'No Aplica')
        indice_marketplace='No Aplica'
    elif len(mplaces)==1:
        indice_marketplace=mplaces[0]
    else:
        mplaces.insert(0,'No Seleccionado')
        indice_marketplace='No Seleccionado'


    return [plataformas,indice_plataforma,mplaces,indice_marketplace]

# Vista principal
def graphics(request):
    option=[]
    name=[]
    tables=[]
    table='{"head":["nombre", "Apellido", "edad"],"data":[["juan", "perez",5],["pedro", "martinez", 6]]}'
    tables.append('id_3')

    #option.append('{"title": {"text": "PIE", "subtext": "grafico 1", "left": "center"}, "tooltip": {"trigger": "item"}, "legend": {"orient": "vertical", "left": "left"}, "series": [{"name": "Red", "data": [{"value": 1176056.0, "name": "Facebook"}, {"value": 34252.0, "name": "Instagram"}, {"value": 148551.0, "name": "Audience Network"}, {"value": 87497.0, "name": "Messenger"}, {"value": 7950.0, "name": "Google"}, {"value": 28951.0, "name": "AdWords"}, {"value": 5379.0, "name": "YouTube"}, {"value": 17946.0, "name": "Eikon"}, {"value": 189.0, "name": "Prensa Libre"}], "type": "pie", "radius": "50%", "emphasis": {"itemStyle": {"shadowBlur": "10", "shadowOffsetX": "0", "shadowColor": "rgba(0, 0, 0, 0.5)"}}}]}')
    option.append('{"title": {"text": "ejempo_0"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    option.append('{"title": {"text": "ejempo_1"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    option.append('{"title": {"text": "ejempo_2"},"xAxis": {"type": "category","data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},"yAxis": {"type": "value"},"series": [{"data": [150, 230, 224, 218, 135, 147, 260],"type": "line","name": "uno"},{"data": [160, 220, 214, 228, 145, 157, 270],"type": "line","name": "dos"}]}')
    name.append('id_0')
    name.append('id_1')
    name.append('id_2')

    table='{"head":["nombre", "Apellido", "edad"],"data":[["juan", "perez",5],["pedro", "martinez", 6]]}'
    stud_obj = json.loads(table)
    head=stud_obj['head']
    data=stud_obj['data']
    html='<div style=" float: left; width: 20%;">'
    html+='<table id="id_3" class="display">'
    html+='<thead>'
    html+='<tr>'
    for enc in head:
        html+='<th>'+enc+'</th>'
    html+='</tr>'
    html+='</thead>'
    html+='<tbody>'
    for row in data:
        html+='<tr>'
        for element in row:
            html+='<td>'+str(element)+'</td>'
        html+='</tr>'
    html+='</tbody>'
    html+='</table>'
    html+='</div>'


    json_option = json.dumps(option)
    json_name = json.dumps(name)
    json_table = json.dumps(tables)

    template_dashboard='<div style=" float: left; width: 20%;"><div id="id_0" style="width:300px; height:300px;"></div></div><div style=" float: left; width: 20%;padding-left: 2em" ><div id="id_1" style="width:300px; height:300px;"></div></div><div style=" float: left; width: 20%;"><div id="id_2" style="width:300px; height:300px;"></div></div>'
    template_dashboard+=html
    context = {
        'options' :json_option ,
        'tables' :json_table,
        'names':json_name,
        'template_dashboard': template_dashboard
    }
    return render(request, "dashboard/graphics.html", context)

#Crear un nuevo dashboard
def newdashboard(request):
    form = DashboardForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            instance=form.save(commit=False)
            instance.user=request.user

            if 'id_rol' in request.POST:
                id_rol=int(request.POST["id_rol"])
                if id_rol>0:
                    rol=Rol.objects.filter(id=id_rol).first()
                    instance.rol=rol
            instance.save()
            asignacion=User_Dashboard.objects.create(user=instance.user, dashboard=instance, edit=1, delete=1)
            asignacion.save()

            messages.success(request, "Dashboard creado exitosamente." )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, "Hubo un error al crear el dashboard.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

#Eliminar un dashboard
def deleteDashboard(request, id):
    dashboard_delete=request.user.Dashboards.filter(id=id)
    if not (dashboard_delete):
        messages.error(request, "No tiene acceso a este lienzo." )
        return redirect ('/')
    else:
        dashboard_delete[0].delete()
        messages.success(request, "Se elimino el dashboard exitosamente." )
        return redirect ('/')

#Eliminar un dashboard desde admin
def deleteDashboardconfig(request, id):
    dashboard_delete=request.user.Dashboards.filter(id=id)
    if not (dashboard_delete):
        messages.error(request, "No tiene acceso a este lienzo." )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        dashboard_delete[0].delete()
        messages.success(request, "Se elimino el dashboard exitosamente." )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

#Crea una nueva fila
def newrow(request):
    id_dashboard=int(request.POST["id_dashboard"])
    if not (request.user.Dashboards.filter(id=id_dashboard)):
        messages.error(request, "No tiene acceso a este lienzo." )
        return redirect ('/')
    else:
        form = RowForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            try:
                instance=form.save(commit=False)
                instance.dashboard=request.user.Dashboards.filter(id=id_dashboard)[0]
                instance.available=instance.column.columns
                instance.save()
                messages.success(request, "Fila creada exitosamente." )
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            except Exception as e:
                messages.error(request, str(e))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Hubo un error la fila.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

#Eliminar una fila
def deleteRow(request, id):
    row_delete=Row.objects.filter(id=id)
    if not (row_delete):
        messages.error(request, "No tiene acceso a esta fila.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        dashboard_delete=request.user.Dashboards.filter(id=row_delete[0].dashboard.id)
        if not (dashboard_delete):
            messages.error(request, "No tiene acceso a la fila del lienzo." )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            row_delete[0].delete()
            messages.success(request, "Se elimino la fila exitosamente." )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

#Cargar la info principal para el dashboard dinamico
def print_dashboard(id_dashboard, request, min, max, edit, delete,tienda,flag,indice,indice_plataforma,indice_marketplace,plataformas,marketplaces,dashboard_flag):
    tiendas=tienda

    if (type(tienda) == list):
        tienda = tienda[indice]

    dashboard=Dashboard.objects.filter(id=id_dashboard).first()
    json_name = json.dumps(dashboard.names())
    #Aqui
    json_option = json.dumps(dashboard.options(min, max,tienda))
    #Aqui
    json_table = json.dumps([])
    json_size = json.dumps(dashboard.sizes())

    template_dashboard=dashboard.to_html(min, max,tienda)

    if dashboard_flag:
        tienda_to_html=[tienda,indice_plataforma,indice_marketplace]
        script_tables=dashboard.to_html2(min, max,tienda_to_html,dashboard_flag)
    else:
        script_tables=dashboard.to_html2(min, max,tienda,dashboard_flag)

    form = RowForm(request.POST or None, request.FILES or None)
    context = {
        'dashboard' :dashboard,
        'template_dashboard': template_dashboard,
        'form' : form,
        'Text':'Create',
        'options' :json_option,
        'names':json_name,
        'tables' :json_table,
        'script_tables' :script_tables,
        'sizes' :json_size,
        'edit' :edit,
        'delete' :delete,
        'stores':tiendas,
        'flag':flag,
		'tienda':tienda,
		'plataformas':plataformas,
		'indice_plataformas':indice_plataforma,
		'marketplaces':marketplaces,
		'indice_marketplaces':indice_marketplace,
        'dashboard_flag':dashboard_flag
    }
    return context

#Se genera la vista para el dashboard dinamico
def dashboard(request):
    id_dashboard=int(request.GET["id_dashboard"])
    if (request.user.rol_id == 4):
        nTiendas = list(Store.objects.filter(status='Activado').values_list('name',flat=True))
    else:
        stores = UserStore.objects.filter(user=request.user.id).values_list('store',flat=True)
        nTiendas = list(Store.objects.filter(pk__in=[stores],status='Activado').values_list('name',flat=True))        

    getTienda =request.GET.get("tienda","")
    getMarketplace =request.GET.get("marketplace","")
    getPlataforma =request.GET.get("plataforma","")

    flag=False
    indice=0
    if(len(nTiendas)==1):
        nTiendas=nTiendas[0]
        flag=False
    elif (len(nTiendas)>1):
        flag=True
    
    if getTienda != "":
        indice = nTiendas.index(getTienda.replace('&amp;','&'))
        flag=True

    min = int(request.GET.get ('min', "0"))
    if min==0:
        if (id_dashboard==2 or id_dashboard==3):
            start_day_of_prev_month= date.today() - timedelta(days=date.today().day-1)
            last_day_of_prev_month= date.today()
        else:
            start_day_of_prev_month = date.today().replace(day = 1)
            last_day_of_prev_month=start_day_of_prev_month.replace(day=list(calendar.monthrange(date.today().year, date.today().month))[1])
        min=str(start_day_of_prev_month)
        max=str(last_day_of_prev_month)
    else:
        date1 = int(request.GET.get ('min', "0"))
        date2 = int(request.GET.get ('max', "0"))
        if date1>0:
            min=str(date1)
            min=min[0:4]+'-'+min[4:6]+'-'+min[6:8]
            max=str(date2)
            max=max[0:4]+'-'+max[4:6]+'-'+max[6:8]
    tienda = nTiendas
    edit=0
    delete=0
    if(request.user.rol=='Admin'):
        edit=1
        delete=1
    else:
        asignacion=User_Dashboard.objects.filter(user=request.user, dashboard_id=id_dashboard).first()
        if (asignacion):
            edit=asignacion.edit
            delete=asignacion.delete
        else:
            dashboard=Dashboard.objects.filter(id=id_dashboard).first()
            if (dashboard.rol):
                if(request.user.rol.id<dashboard.rol.id):
                    messages.error(request, "No tiene acceso a este lienzo." )
                    return redirect ('/')
            else:
                messages.error(request, "No tiene acceso a este lienzo." )
                return redirect ('/')

    if (type(tienda) == list):
        tienda_str = tienda[indice]
    else:
        tienda=[tienda]
        tienda_str=tienda[0]

    filtros_tienda=obtener_filtros_tienda(tienda_str,min,max)
    if getMarketplace != "":
        indice_marketplace=getMarketplace
    else:
        indice_marketplace=filtros_tienda[3]

    if getPlataforma != "":
        indice_plataforma=getPlataforma
    else:
        indice_plataforma=filtros_tienda[1]
    plataformas=filtros_tienda[0]
    marketplaces=filtros_tienda[2]
    if id_dashboard==8:
        flag_dashboard=True
    else:
        flag_dashboard=False

    context=print_dashboard(id_dashboard, request, min, max, edit, delete,tienda,flag,indice,indice_plataforma,indice_marketplace,plataformas,marketplaces,flag_dashboard)
    return render(request, "dashboard/dashboard_dinamico.html", context)