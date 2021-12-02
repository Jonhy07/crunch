from django.shortcuts import render
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.contrib import messages
from pool_energy_app import graphs
from pool_energy_app.filter.models import Filter, Type_comparation
from pool_energy_app.graphs.forms import BarXForm2, GraphForm, PieForm, BarXForm, YRow2Form, YRowForm, TabTypeForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Graph, Graph_Filter, Type_agrupation, Type_icon, YRow
from pool_energy_app.charts.models import Dashboard, Row, User_Dashboard
from pool_energy_app.graphs.models import Type_calculate
from pool_energy_app.endpoint.models import Detail

#CONVERTIR QUERYSET EN OPCCIONES
def convertir(queryset, string):
    text=''
    if (string):
        text='<option value="" selected="">'+string+'</option>'
    else:
        text='<option value="" selected="">Please select the count value.</option>'
    for item in queryset:
        text+='<option value='+str(item.id)+'>'+str(item)+'</option>'
    return text


#-------------------------------VALIDAR SEGURIDAD DE UNA  GRAFICA
#Seguridad del dashboard:
def validar_Dashboard(request, id_dashboard ):
    dashboard=Dashboard.objects.filter(id=id_dashboard)
    if(dashboard):
       dashboard=dashboard.first()
    else:
        return {'bandera' : True }
    if(request.user.rol.rol=='Admin'):
        return {'bandera' : False, 'edit':1, 'delete':1, 'dashboard':dashboard}
    else:
        asignacion=User_Dashboard.objects.filter(user=request.user, dashboard_id=id_dashboard)
        if asignacion:
            asignacion=asignacion.first()
            return {'bandera' : False, 'edit':(asignacion.edit*request.user.rol.create), 'delete':(asignacion.delete*request.user.rol.create), 'dashboard':dashboard }
        else:
            if (dashboard.rol):
                if(request.user.rol.id<dashboard.rol.id):
                    return {'bandera' : True, 'dashboard':dashboard }
                else:
                    return {'bandera' : False, 'edit':0, 'delete':0, 'dashboard':dashboard }
            else:
                return {'bandera' : True, 'dashboard':dashboard }


#Validacion de la Grafica para modificarla
def validar_Grafica(request, id):
    graph_update=Graph.objects.filter(id=id)
    if not (graph_update):
        messages.error(request, "Aun no se crea la grafica.")
        return {'bandera' : True }
    else:
        diccionario=validar_Dashboard(request, graph_update[0].row.dashboard.id )
        #dashboard_graph=request.user.Dashboards.filter(id=graph_update[0].row.dashboard.id)    
        if (diccionario['bandera']):
            messages.error(request, "No tiene acceso a esta grafica." )
            return {'bandera' : True }
        else:
            graph=graph_update[0]
            if(graph.finish):
                messages.error(request, "No es posible modificar esta grafica." )
                return {'bandera' : True }
            else:
                return {'bandera' : False, 'graph':graph}


#Validacion de la Grafica para modificarla
def validar_Grafica_Filtros(request, id):
    graph_update=Graph.objects.filter(id=id)
    if not (graph_update):
        messages.error(request, "Aun no se crea la grafica.")
        return {'bandera' : True }
    else:
        #dashboard_graph=request.user.Dashboards.filter(id=graph_update[0].row.dashboard.id)
        diccionario=validar_Dashboard(request, graph_update[0].row.dashboard.id ) 
        if (diccionario['bandera']):
            messages.error(request, "No tiene acceso a esta grafica." )
            return {'bandera' : True }
        else:
            graph=graph_update[0]
            return {'bandera' : False, 'graph':graph}


#-------------------------------NUEVA GRAFICA
#Vista para una nueva grafica
def newgraph(request, id):
    row_add_graph=Row.objects.filter(id=id)
    if not (row_add_graph):
        messages.error(request, "No tiene acceso a esta fila.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        diccionario=validar_Dashboard(request, row_add_graph[0].dashboard.id )
        #dashboard_add_graph=request.user.Dashboards.filter(id=row_add_graph[0].dashboard.id) 
        if (diccionario['bandera']):
            messages.error(request, "No tiene acceso a la fila del lienzo." )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            rows=row_add_graph[0].available
            form = GraphForm(request.POST or None, request.FILES or None, rows=rows, user=request.user)
            context = {
                'form':form,
                'row': row_add_graph[0],
                'Text':'Create'
            }
            return render(request, "graph/newgraph.html", context)


#Agregar una grafica
def addgraph(request):
    id_row=int(request.POST["id_row"])
    rows=Row.objects.filter(id=id_row)
    form = GraphForm(request.POST or None, request.FILES or None, rows=rows[0].available, user=request.user)
    if form.is_valid():
        if not (rows):
            messages.error(request, "La Fila no existe")
            return redirect ('/')
        else:
            row=rows[0]
            diccionario=validar_Dashboard(request, row.dashboard.id )
            #if not (request.user.Dashboards.filter(id=row.dashboard.id)):
            if (diccionario['bandera']):
                messages.error(request, "No tiene acceso a la fila del lienzo.")
                return redirect('/')
            else:
                if (row.available<1):
                    messages.error(request, "Ya no puede agregar graficas a esta fila.")
                    return redirect('/dashboard/?id_dashboard='+str(row.id))
                else:
                    try:
                        instance=form.save(commit=False)
                        if(instance.column>row.available):
                            messages.error(request, "El numero de columnas supera las existentes")
                            return redirect('/dashboard/?id_dashboard='+str(row.id))
                        else:
                            instance.row=row
                            if(instance.type_graph.pk==0):
                                instance.finish=True
                            instance.save()
                            row.available=(row.available-instance.column)
                            row.save()
                            if instance.type_graph.pk==1:
                                return redirect('/dashboard/row/graph/add/{}/bar'.format(instance.pk))
                            elif instance.type_graph.pk==2:
                                return redirect('/dashboard/row/graph/add/{}/bar'.format(instance.pk))
                            elif instance.type_graph.pk==3:
                                return redirect('/dashboard/row/graph/add/{}/bar'.format(instance.pk))
                            elif instance.type_graph.pk==4:
                                return redirect('/dashboard/row/graph/add/{}/pie'.format(instance.pk))
                            elif instance.type_graph.pk==5:
                                return redirect('/dashboard/row/graph/add/{}/tab'.format(instance.pk))
                            elif instance.type_graph.pk==6:
                                return redirect('/dashboard/row/graph/add/{}/card'.format(instance.pk))
                            elif instance.type_graph.pk==7:
                                return redirect('/dashboard/row/graph/add/{}/barconcat'.format(instance.pk))
                            else:
                                messages.success(request, "Grafico creado exitosamente.")
                                return redirect('/dashboard/?id_dashboard='+str(row.dashboard.id))
                    except Exception as e:
                        messages.error(request, str(e))
                        return redirect('/dashboard/?id_dashboard='+str(row.dashboard.id))

#-------------------------------PIE
#Vista para seleccionar el campo de agrupacion del pie
def pie(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        form = PieForm(request.POST or None, request.FILES or None, endpoint=graph.endpoint)
        type_calculate=Type_calculate.objects.all()
        yrowL=Detail.objects.filter(endpoint=graph.endpoint)
        yrow=convertir(yrowL, None)
        yrowfL=Detail.objects.filter(endpoint=graph.endpoint).exclude(type_detail=3).exclude(type_detail=4)
        yrowf=convertir(yrowfL, None)

        context = {
            'form':form,
            'Text':'Create',
            'graph':graph,
            'type_calculate': type_calculate,
            'yrow': yrow,
            'yrowf': yrowf
        }
        return render(request, "graph/pie/pie.html", context)

#Recibiendo el formulario de  pie para el update
def update_pie(request):
    id_graph=int(request.POST["id_graph"])
    graphs=Graph.objects.filter(id=id_graph)
    #value=Detail.objects.filter(id=request.POST["yrow"]).first()
    #type_calculate=Type_calculate.objects.filter(id=request.POST["type_calculate"]).first()

    form = PieForm(request.POST or None, request.FILES or None, endpoint=graphs[0].endpoint)
    if form.is_valid():
        diccionario=validar_Grafica(request, id_graph)
        bandera=diccionario['bandera']
        if(bandera):
            return redirect('/')
        else:
            graph=diccionario['graph']
            instance=form.save(commit=False)
            #yrow=YRow.objects.create(name="pie", graph=graph, value=value, type_calculate=type_calculate)
            yrow=YRow.objects.create(name="pie", graph=graph, value_id=request.POST["yrow"], type_calculate_id=request.POST["type_calculate"])
            graph.xrow=instance.xrow
            graph.send=PieToJson(graph, yrow)
            graph.finish=True
            graph.save()
            yrow.save()
            bandera = bool(request.POST.get('filtros', '') == 'on')
            
            if (bandera) :
                messages.success(request, "Grafico creado exitosamente. Detalle sus filtros.")
                return redirect('/dashboard/row/graph/add/{}/filter/pie'.format(graph.pk))
            messages.success(request, "Grafico creado exitosamente.")
            return redirect('/dashboard/?id_dashboard='+str(graph.row.dashboard.id))


#-------------------------------BAR

#Vista para seleccionar los datos de la  bar
def bar(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        form = BarXForm(request.POST or None, request.FILES or None, endpoint=graph.endpoint)
        eje="X"
        eje2="Y"
        if graph.type_graph.id==3:
            eje="Y"
            eje2="X"


        context = {
            'type':(str(graph.type_graph)).lower(),
            'form':form,
            'Text':'Save',
            'graph':graph,
            'eje':eje,
            'eje2':eje2
        }
        return render(request, "graph/bar/bar.html", context)


def barconcat(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        form = BarXForm2(request.POST or None, request.FILES or None, endpoint=graph.endpoint)
        eje="X"
        eje2="Y"
        if graph.type_graph.id==3:
            eje="Y"
            eje2="X"


        context = {
            'type':(str(graph.type_graph)).lower(),
            'form':form,
            'Text':'Save',
            'graph':graph,
            'eje':eje,
            'eje2':eje2
        }
        return render(request, "graph/bar/barconcat.html", context)


#Recibiendo el formulario de la bar para el update
def update_bar(request):
    id_graph=int(request.POST["id_graph"])
    graphs=Graph.objects.filter(id=id_graph)

    form = BarXForm(request.POST or None, request.FILES or None, endpoint=graphs[0].endpoint)
    if form.is_valid():
        diccionario=validar_Grafica(request, id_graph)
        bandera=diccionario['bandera']
        if(bandera):
            return redirect('/')
        else:
            graph=diccionario['graph']
            instance=form.save(commit=False)
            graph.xrow=instance.xrow
            graph.type_agrupation=instance.type_agrupation
            graph.type_time_agrupation=instance.type_time_agrupation
            graph.save()

            messages.success(request, "Guardado exitosamente por favor siga detallando la grafica")
            if graph.type_agrupation.id==1:
                return redirect('/dashboard/row/graph/add/{}/bar/legend'.format(graph.pk))
            else:
                return redirect('/dashboard/row/graph/add/{}/bar/name'.format(graph.pk))


def update_barconcat(request):
    id_graph=int(request.POST["id_graph"])
    graphs=Graph.objects.filter(id=id_graph)

    form = BarXForm2(request.POST or None, request.FILES or None, endpoint=graphs[0].endpoint)
    if form.is_valid():
        diccionario=validar_Grafica(request, id_graph)
        bandera=diccionario['bandera']
        if(bandera):
            return redirect('/')
        else:
            graph=diccionario['graph']
            instance=form.save(commit=False)
            graph.xrow=instance.xrow
            graph.type_agrupation=Type_agrupation.objects.filter(pk=1).first()
            graph.type_time_agrupation=instance.type_time_agrupation
            graph.save()

            messages.success(request, "Guardado exitosamente por favor siga detallando la grafica")
            return redirect('/dashboard/row/graph/add/{}/bar/legend'.format(graph.pk))


#Formulario para  la bar legend
def legend(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        type_calculate=Type_calculate.objects.all()
        yrowL=Detail.objects.filter(endpoint=graph.endpoint)
        yrow=convertir(yrowL, None)
        yrowfL=Detail.objects.filter(endpoint=graph.endpoint).exclude(type_detail=3).exclude(type_detail=4)
        yrowf=convertir(yrowfL, None)
        legend=Detail.objects.filter(endpoint=graph.endpoint, type_detail=3)
        eje="Y"
        eje2="X"
        if graph.type_graph.id==3:
            eje="X"
            eje2="Y"

        context = {
            'Text':'Create',
            'type':(str(graph.type_graph)).lower(),
            'graph':graph,
            'type_calculate': type_calculate,
            'yrow': yrow,
            'yrowf': yrowf,
            'legend': legend,
            'eje':eje,
            'eje2':eje2

        }
        return render(request, "graph/bar/legend.html", context)


#Guardar la barra legend
def create_bar_legend(request):
    id_graph=int(request.POST["id_graph"])
    #value=Detail.objects.filter(id=request.POST["yrow"]).first()
    #type_calculate=Type_calculate.objects.filter(id=request.POST["type_calculate"]).first()

    diccionario=validar_Grafica(request, id_graph)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        #yrow=YRow.objects.create(name=request.POST["legend"], graph=graph, value=value, type_calculate=type_calculate)
        yrow=YRow.objects.create(name=request.POST["legend"], graph=graph, value_id=request.POST["yrow"], type_calculate_id=request.POST["type_calculate"])
        graph.send=BarLegendToJson(graph, yrow)
        graph.finish=True
        graph.save()
        yrow.save()
        bandera = bool(request.POST.get('filtros', '') == 'on')
        
        if (bandera) :
            messages.success(request, "Grafico creado exitosamente. Detalle sus filtros.")
            return redirect('/dashboard/row/graph/add/{}/filter/bar'.format(graph.pk))

        messages.success(request, "Grafico creado exitosamente.")
        return redirect('/dashboard/?id_dashboard='+str(graph.row.dashboard.id))



#Formulario para  la bar Nombre
def namebar(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        #yrowL=Detail.objects.filter(endpoint=graph.endpoint).exclude(id__in=YRow.objects.filter(graph=graph).values_list('value').all())
        yrowL=Detail.objects.filter(endpoint=graph.endpoint)
        yrow=convertir(yrowL, None)
        #yrowfL=Detail.objects.filter(endpoint=graph.endpoint).exclude(type_detail=3).exclude(type_detail=4).exclude(id__in=YRow.objects.filter(graph=graph).values_list('value').all())
        yrowfL=Detail.objects.filter(endpoint=graph.endpoint).exclude(type_detail=3).exclude(type_detail=4)
        yrowf=convertir(yrowfL, None)
        form = YRowForm(request.POST or None, request.FILES or None)
        yrows=YRow.objects.filter(graph=graph)
        eje="Y"
        eje2="X"
        if graph.type_graph.id==3:
            eje="X"
            eje2="Y"

        context = {
            'Text':'Add',
            'type':(str(graph.type_graph)).lower(),
            'graph':graph,
            'yrow': yrow,
            'yrowf': yrowf,
            'yrows': yrows,
            'form': form,
            'eje':eje,
            'eje2':eje2
        }
        return render(request, "graph/bar/name.html", context)



#Guardar la Yrow de la grafica
def add_yrow(request):
    id_graph=int(request.POST["id_graph"])
    value=Detail.objects.filter(id=request.POST["yrow"]).first()
    form = YRowForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        diccionario=validar_Grafica(request, id_graph)
        bandera=diccionario['bandera']
        if(bandera):
            return redirect('/')
        else:
            graph=diccionario['graph']
            instance=form.save(commit=False)
            instance.graph=graph
            instance.value=value
            instance.save()
            messages.success(request, "Columna Agregada Exitosamente.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



#Guardar la barra name
def create_bar_name(request):
    id_graph=int(request.POST["id_graph"]) 
    diccionario=validar_Grafica(request, id_graph)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        graph.send=BarNameToJson(graph)
        graph.finish=True
        graph.save()
        bandera = bool(request.POST.get('filtros', '') == 'on')
        
        if (bandera) :
            messages.success(request, "Grafico creado exitosamente. Detalle sus filtros.")
            return redirect('/dashboard/row/graph/add/{}/filter/bar'.format(graph.pk))

        messages.success(request, "Grafico creado exitosamente.")
        return redirect('/dashboard/?id_dashboard='+str(graph.row.dashboard.id))


#-------------------------------CARD
#Vista para seleccionar el campo de agrupacion del pie
def card(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        type_agrupation=Type_agrupation.objects.all()
        type_calculate=Type_calculate.objects.all()
        type1=convertir(type_calculate, None)
        type_calculate=Type_calculate.objects.exclude(id=2).exclude(id=3)
        type2=convertir(type_calculate, None)


        type_icon=Type_icon.objects.all()
        yrowL=Detail.objects.filter(endpoint=graph.endpoint)
        yrow=convertir(yrowL, None)
        yrowfL=Detail.objects.filter(endpoint=graph.endpoint).exclude(type_detail=3).exclude(type_detail=4)
        yrowf=convertir(yrowfL, None)

        context = {
            'Text':'Create',
            'graph':graph,
            'type_agrupation': type_agrupation,
            #'type_calculate': type_calculate,
            'type1': type1,
            'type2': type2,
            'type_icon': type_icon,
            'yrow': yrow,
            'yrowf': yrowf
        }
        return render(request, "graph/card/card.html", context)

#Recibiendo el formulario de  card para el update
def update_card(request):
    id_graph=int(request.POST["id_graph"])
        #graphs=Graph.objects.filter(id=id_graph)
    #value=Detail.objects.filter(id=request.POST["yrow"]).first()
    #type_calculate=Type_calculate.objects.filter(id=request.POST["type_calculate"]).first()
    type_icon=Type_icon.objects.filter(id=request.POST["type_icon"]).first()
    type_agrupation=Type_agrupation.objects.filter(id=request.POST["type_agrupation"]).first()

    
    
    diccionario=validar_Grafica(request, id_graph)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        #yrow=YRow.objects.create(name="card", graph=graph, value=value, type_calculate=type_calculate)
        yrow=YRow.objects.create(name="card", graph=graph, value_id=request.POST["yrow"], type_calculate_id=request.POST["type_calculate"])
        graph.type_icon=type_icon
        graph.type_agrupation=type_agrupation
        graph.send=CardToJson(graph, yrow)
        graph.finish=True
        graph.save()
        yrow.save()
        bandera = bool(request.POST.get('filtros', '') == 'on')
        if (bandera) :
            messages.success(request, "Grafico creado exitosamente. Detalle sus filtros.")
            return redirect('/dashboard/row/graph/add/{}/filter/card'.format(graph.pk))

        messages.success(request, "Grafico creado exitosamente.")
        return redirect('/dashboard/?id_dashboard='+str(graph.row.dashboard.id))


#-------------------------------TAB

#Vista para seleccionar los datos de la tabla
def tab(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        form = TabTypeForm(request.POST or None, request.FILES or None)
        context = {
            'type':(str(graph.type_graph)).lower(),
            'form':form,
            'Text':'Save',
            'graph':graph
        }
        return render(request, "graph/tab/tab.html", context)



#Recibiendo el formulario de la tab para el update
def update_tab(request):
    id_graph=int(request.POST["id_graph"])
    form = TabTypeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        diccionario=validar_Grafica(request, id_graph)
        bandera=diccionario['bandera']
        if(bandera):
            return redirect('/')
        else:
            graph=diccionario['graph']
            instance=form.save(commit=False)
            graph.type_agrupation=instance.type_agrupation
            graph.save()
            messages.success(request, "Guardado exitosamente por favor siga detallando la grafica")
            if graph.type_agrupation.id==1:
                return redirect('/dashboard/row/graph/add/{}/tab/legend'.format(graph.pk))
            else:
                return redirect('/dashboard/row/graph/add/{}/tab/name'.format(graph.pk))


#Formulario para  la tab Nombre
def nametab(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        #yrow=Detail.objects.filter(endpoint=graph.endpoint)
        form = YRow2Form(request.POST or None, request.FILES or None, endpoint=graph.endpoint)
        yrows=YRow.objects.filter(graph=graph)
        context = {
            'Text':'Add',
            'type':(str(graph.type_graph)).lower(),
            'graph':graph,
            'form': form,
            'yrows': yrows,
        }
        return render(request, "graph/tab/name.html", context)



#Guardar la Yrow de la tabla
def add_col(request):
    id_graph=int(request.POST["id_graph"])
    diccionario=validar_Grafica(request, id_graph)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        form = YRow2Form(request.POST or None, request.FILES or None, endpoint=graph.endpoint)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.graph=graph
            instance.save()
            messages.success(request, "Columna Agregada Exitosamente.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


#Guardar la tab col
def create_tab_name(request):
    id_graph=int(request.POST["id_graph"]) 
    diccionario=validar_Grafica(request, id_graph)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        graph.send=TabColumnToJson(graph)
        graph.finish=True
        graph.save()
        bandera = bool(request.POST.get('filtros', '') == 'on')
        #bandera = bool( ('filtros', "falso"))
        if (bandera) :
            messages.success(request, "Grafico creado exitosamente. Detalle sus filtros.")
            return redirect('/dashboard/row/graph/add/{}/filter/bar'.format(graph.pk))

        messages.success(request, "Grafico creado exitosamente.")
        return redirect('/dashboard/?id_dashboard='+str(graph.row.dashboard.id))


#Formulario para  la tab Nombre
def legendtab(request, id):
    diccionario=validar_Grafica(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        yrows=YRow.objects.filter(graph=graph)
        type_calculate=Type_calculate.objects.all()
        yrowL=Detail.objects.filter(endpoint=graph.endpoint)
        yrow=convertir(yrowL, None)
        yrowfL=Detail.objects.filter(endpoint=graph.endpoint).exclude(type_detail=3).exclude(type_detail=4)
        yrowf=convertir(yrowfL, None)

        context = {
            'Text':'Add',
            'type':(str(graph.type_graph)).lower(),
            'graph':graph,
            'yrows': yrows,
            'type_calculate': type_calculate,
            'yrow': yrow,
            'yrowf': yrowf,
        }
        return render(request, "graph/tab/legend.html", context)



#Guardar la Yrow de la tabla legend
def add_col_legend(request):
    id_graph=int(request.POST["id_graph"])
    diccionario=validar_Grafica(request, id_graph)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']

        #value=Detail.objects.filter(id=request.POST["yrow"]).first()
        yrow=None
        if request.POST["type_calculate"]!="0":
            #type_calculate=Type_calculate.objects.filter(id=request.POST["type_calculate"]).first()
            #yrow=YRow.objects.create(name=request.POST["name"], graph=graph, value=value, type_calculate=type_calculate)
            yrow=YRow.objects.create(name=request.POST["name"], graph=graph, value_id=request.POST["yrow"], type_calculate_id=request.POST["type_calculate"])
        else:
            #yrow=YRow.objects.create(name=request.POST["name"], graph=graph, value=value)
            yrow=YRow.objects.create(name=request.POST["name"], graph=graph, value_id=request.POST["yrow"])
        yrow.save()
        messages.success(request, "Columna Agregada Exitosamente.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



#-------------------------------OPCIONES PARA LA GRAFICA
#Eliminar una grafica
def deletegraph(request, id):
    graphs=Graph.objects.filter(id=id)
    if not (graphs):
        messages.error(request, "No existe la grafica.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        graph=graphs[0]
        rows=Row.objects.filter(id=graph.row.id)
        row=rows[0]

        diccionario=validar_Dashboard(request, row.dashboard.id )
        #if not (request.user.Dashboards.filter(id=row.dashboard.id)):
        if (diccionario['bandera']):
            messages.error(request, "No tiene acceso a la fila del lienzo.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            row.available=row.available+graph.column
            graph.delete()
            row.save()
            messages.success(request, "Se elimino la grafica exitosamente." )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



#crear json del pie
def PieToJson (graph, yrow):
    txt='{'
    txt+='"dataset": "'+graph.endpoint.name_db+'",'
    txt+='"x":"'+graph.xrow.name_db+'",'
    txt+='"y":{'
    txt+='"value": "'+yrow.value.name_db+'",'
    txt+='"calculate": "'+yrow.type_calculate.value+'"'
    txt+='}'
    txt+='}'
    return json.loads(txt)

#crear json de la bar legend
def BarLegendToJson (graph, yrow):
    txt='{'
    txt+='"dataset": "'+graph.endpoint.name_db+'",'
    txt+='"type": "'+str(graph.type_agrupation.id)+'",'
    txt+='"type_time": "'+str(graph.type_time_agrupation.id)+'",'
    txt+='"x":"'+graph.xrow.name_db+'",'
    txt+='"y":['
    txt+='{'
    txt+='"name": "'+yrow.name+'",'
    txt+='"value": "'+yrow.value.name_db+'",'
    txt+='"calculate": "'+yrow.type_calculate.value+'"'
    txt+='}'
    txt+=']'
    txt+='}'
    return json.loads(txt)


def BarNameToJson (graph):
    txt='{'
    txt+='"dataset": "'+graph.endpoint.name_db+'",'
    txt+='"type": "'+str(graph.type_agrupation.id)+'",'
    txt+='"type_time": "'+str(graph.type_time_agrupation.id)+'",'
    txt+='"x":"'+graph.xrow.name_db+'",'
    txt+='"y":['
    Yrows=YRow.objects.filter(graph=graph)

    for row in Yrows:
        txt+='{'
        txt+='"name": "'+row.name+'",'
        txt+='"value": "'+row.value.name_db+'",'
        txt+='"calculate": "'+row.type_calculate.value+'"'
        txt+='},'
    txt = txt[:-1]
    txt+=']'
    txt+='}'
    return json.loads(txt)

#crear json de la card
def CardToJson (graph, yrow):
    txt='{'
    txt+='"dataset": "'+graph.endpoint.name_db+'",'
    txt+='"type": "'+str(graph.type_agrupation.id)+'",'
    txt+='"columns":['
    txt+='{"field": "'+yrow.value.name_db+'",'
    txt+='"calculate": "'+yrow.type_calculate.value+'"}'
    txt+=']'
    txt+='}'
    return json.loads(txt)


def TabColumnToJson (graph):
    txt='{'
    txt+='"dataset": "'+graph.endpoint.name_db+'",'
    txt+='"type": "'+str(graph.type_agrupation.id)+'",'
    txt+='"columns":['
    Yrows=YRow.objects.filter(graph=graph).order_by('id')
    if (graph.type_agrupation.id==1):
        for row in Yrows:
            if (row.type_calculate):
                txt+='{'
                txt+='"field": "'+row.value.name_db+'",'
                txt+='"calculate": "'+row.type_calculate.value+'"'
                txt+='},'
            else:
                txt+='{'
                txt+='"field": "'+row.value.name_db+'"'
                txt+='},'
    else:
        for row in Yrows:
            txt+='{'
            txt+='"field": "'+row.value.name_db+'"'
            txt+='},'
    txt = txt[:-1]
    txt+=']'
    txt+='}'
    return json.loads(txt)







#--------------FILTROS
#--Filter legend bar y name bar, legend tab, name tab
def filterlegendbar(request, id):
    diccionario=validar_Grafica_Filtros(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        filter=Filter.objects.all()
        eje="Y"
        eje2="X"
        if graph.type_graph.id==3:
            eje="X"
            eje2="Y"
        filters=Graph_Filter.objects.filter(graph=graph)

        context = {
            'Text':'Add',
            'type':(str(graph.type_graph)).lower(),
            'graph':graph,
            'eje':eje,
            'eje2':eje2,
            'filter':filter,
            'filters':filters
        }
        return render(request, "graph/bar/legendfilter.html", context)


def filterlegendpie(request, id):
    diccionario=validar_Grafica_Filtros(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        filter=Filter.objects.all()
        eje="Y"
        eje2="X"
        if graph.type_graph.id==3:
            eje="X"
            eje2="Y"
        filters=Graph_Filter.objects.filter(graph=graph)

        context = {
            'Text':'Add',
            'type':(str(graph.type_graph)).lower(),
            'graph':graph,
            'eje':eje,
            'eje2':eje2,
            'filter':filter,
            'filters':filters
        }
        return render(request, "graph/pie/piefilter.html", context)


#--Filter legend bar y name bar
def filterlegendcard(request, id):
    diccionario=validar_Grafica_Filtros(request, id)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        yrow=YRow.objects.filter(graph=graph).first()
        filter=Filter.objects.all()
        filters=Graph_Filter.objects.filter(graph=graph)
        context = {
            'Text':'Add',
            'type':(str(graph.type_graph)).lower(),
            'graph':graph,
            'filter':filter,
            'filters':filters,
            'row': yrow
        }
        return render(request, "graph/card/cardfilter.html", context)

#------------FILTRO GENERAL

#Create Filter
def create_filter(request):
    id_graph=int(request.POST["id_graph"])
    id_filter=int(request.POST["filter"])
    id_value=int(request.POST["value"])
    diccionario=validar_Grafica_Filtros(request, id_graph)
    bandera=diccionario['bandera']
    if(bandera):
        return redirect('/')
    else:
        graph=diccionario['graph']
        filter=Filter.objects.filter(id=id_filter).first()
        #detail=Detail.objects.filter(id=id_value).first()
        comparate_value=None
        type_comparation=None
        #Aqui se va a modificar si hay otros filtros
        if (filter.type_filter.pk==2):
            if (filter.type_detail.pk==4):
                comparate_value=filter.detail
                type_comparation=Type_comparation.objects.filter(id=3).first()
        elif (filter.type_filter.pk==1):
            type_comparation=Type_comparation.objects.filter(id=1).first()

                
        #graph_filter=Graph_Filter.objects.create(comparate_value=comparate_value, value=detail, graph=graph, filter=filter, type_comparation=type_comparation)
        graph_filter=Graph_Filter.objects.create(comparate_value=comparate_value, value_id=id_value, graph=graph, filter_id=id_filter, type_comparation=type_comparation)
        graph_filter.save()
        messages.success(request, "Filtro Agregado Exitosamente.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

#Guardar la barra name
def filter_finsh(request):
    id_graph=int(request.POST["id_graph"]) 
    graph=Graph.objects.filter(id=id_graph).first()
    messages.success(request, "Grafico creado exitosamente.")
    return redirect('/dashboard/?id_dashboard='+str(graph.row.dashboard.id))
        

#AJAX:
def filtercampo(request,*args, **kwargs):
    filter=Filter.objects.filter(id=kwargs.get('id_filtro')).first()
    graph=Graph.objects.filter(id=kwargs.get('id_graph')).first()
    detail=list(Detail.objects.filter(type_detail=filter.type_detail, endpoint=graph.endpoint))
    campos=convertir(detail, 'Please select column.')
    return JsonResponse({'data':campos})