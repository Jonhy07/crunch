from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import json
from django.contrib import messages
from requests.api import options
from pool_energy_app.charts.forms import DashboardForm, RowForm
from django.shortcuts import render, redirect, get_object_or_404

from pool_energy_app.users.models import Rol
from pool_energy_app.forms.models import UserStore,Store
from .models import Dashboard, Row, User_Dashboard
import json

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
def print_dashboard(id_dashboard, request, min, max, edit, delete,tienda,flag,indice):
    print(len(tienda))
    tiendas=tienda
    if len(tienda)>1:
        tienda = tienda[indice]
    dashboard=Dashboard.objects.filter(id=id_dashboard).first()
    json_name = json.dumps(dashboard.names())
    #Aqui
    json_option = json.dumps(dashboard.options(min, max,tienda))
    #Aqui
    json_table = json.dumps([])
    json_size = json.dumps(dashboard.sizes())
    template_dashboard=dashboard.to_html(min, max,tienda)
    script_tables=dashboard.to_html2(min, max,tienda)

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
        'flag':flag
    }
    return context



#Se genera la vista para el dashboard dinamico
def dashboard(request):
    id_dashboard=int(request.GET["id_dashboard"])
    stores = UserStore.objects.filter(user=request.user.id).values_list('store',flat=True)
    nTiendas = list(Store.objects.filter(pk__in=[stores]).values_list('name',flat=True))
    getTienda =request.GET.get("tienda","")
    flag=False
    indice=0
    if(len(nTiendas)==1):
        nTiendas=nTiendas[0]
        flag=False
    elif (len(nTiendas)>1):
        flag=True
    
    if getTienda != "":
        indice = nTiendas.index(getTienda)
        flag=True
    min=None
    max=None
    edit=0
    delete=0
    date1 = int(request.GET.get ('min', "0"))
    date2 = int(request.GET.get ('max', "0"))
    tienda = nTiendas#request.GET.get('tienda','')
    if date1>0:
        min=str(date1)
        min=min[0:4]+'-'+min[4:6]+'-'+min[6:8]
        max=str(date2)
        max=max[0:4]+'-'+max[4:6]+'-'+max[6:8]

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

    context=print_dashboard(id_dashboard, request, min, max, edit, delete,tienda,flag,indice)
    return render(request, "dashboard/dashboard_dinamico.html", context)