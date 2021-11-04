from django.contrib.messages.api import error
from django.db import models
from pool_energy_app.charts.models import Row
from pool_energy_app.endpoint.models import Endpoint, Detail
from pool_energy_app.filter.models import Filter, Type_comparation

import requests
import json 
import os
from django.http import response

# Create your models here.

class Type_icon (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    icon = models.CharField(max_length=250)
    color = models.CharField(max_length=250)
    def __str__(self):
        return "%s" % (self.name)

class Type_time_agrupation (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    def __str__(self):
        return "%s" % (self.name)

class Type_graph (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    icon = models.CharField(max_length=250)
    def __str__(self):
        return "%s" % (self.name)


class Type_agrupation (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    card = models.CharField(max_length=250, null=True)
    def __str__(self):
        return "%s" % (self.name)

class Type_calculate (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=50)
    def __str__(self):
        return "%s" % (self.name)


class Graph (models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    column= models.IntegerField(null=False)
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name='Row')
    type_graph = models.ForeignKey(Type_graph, on_delete=models.CASCADE, related_name='Type_graph')
    type_icon = models.ForeignKey(Type_icon, on_delete=models.CASCADE, related_name='Type_icon', null=True)
    type_time_agrupation = models.ForeignKey(Type_time_agrupation, on_delete=models.CASCADE, related_name='Type_time_agrupation', null=True)
    endpoint = models.ForeignKey(Endpoint,  on_delete=models.CASCADE, related_name='Endpoint')
    xrow=models.ForeignKey(Detail,  on_delete=models.CASCADE, related_name='Detail_X', null=True)
    type_agrupation = models.ForeignKey(Type_agrupation, on_delete=models.CASCADE, related_name='Type_agrupation', null=True)
    finish=models.BooleanField(default=False)
    send=models.JSONField(null=True)

    def __str__(self):
        return "%s" % (self.title)
    def get_update_url(self):
        return"/row/graph/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/row/graph/{}/delete".format(self.pk)
    def name(self):
        return ('id_'+str(self.id))
    def send_json(self, min=None, max=None):
        filters=Graph_Filter.objects.filter(graph=self)
        send=''
        send=self.send
        send['filters']=[]
        for filter in filters:
            if filter.filter.type_filter.id==1:
                if min :
                    send['filters'].append({'field':filter.value.name_db, 'equal':filter.type_comparation.signo, 'value':'\''+min+'\''}) 
                    send['filters'].append({'field':filter.value.name_db, 'equal':'<', 'value':'\''+max+'\''})
            else:
                send['filters'].append({'field':filter.value.name_db, 'equal':filter.type_comparation.signo, 'value':filter.comparate_value})
        return send


    def to_html(self, min=None, max=None):
        html="<div class=\"col-"+str (self.column*self.row.column.value)+"\" style=\"height: "+str(self.row.high.value)+"em;\">"
        if (self.type_graph.id<1):
            html+='<div class="dropdown float-end toolsrow hideme">'
            html+='<a href="#" class=" arrow-none card-drop" data-bs-toggle="dropdown" aria-expanded="false">'
            html+='<i class="mdi mdi-dots-vertical"></i>'
            html+='</a>'
            html+='<div class="dropdown-menu dropdown-menu-end">'
            html+="<a  class=\"dropdown-item notify-item delete\" title=\"Eliminar Grafico\" href=\"/dashboard"+self.get_delete_url()+"\"  onclick=\"return confirm('Esta accion borrara la grafica')\">"
            html+="<i class=\"bi bi-trash\" style=\"padding-right: 10%;\"></i>"
            html+="Gráfica</a>"
            html+='</div>'
            html+='</div>'
        else:
            html+='<div class="widget-rounded-circle card" style="height: '+str(self.row.high.value)+'em;">'
            html+='<div class="card-body">'

            html+='<div class="dropdown float-end toolsrow hideme">'
            html+='<a href="#" class=" arrow-none card-drop" data-bs-toggle="dropdown" aria-expanded="false">'
            html+='<i class="mdi mdi-dots-vertical"></i>'
            html+='</a>'
            html+='<div class="dropdown-menu dropdown-menu-end">'
            html+="<a  class=\"dropdown-item notify-item delete\" title=\"Eliminar Grafico\" href=\"/dashboard"+self.get_delete_url()+"\"  onclick=\"return confirm('Esta accion borrara la grafica')\">"
            html+="<i class=\"bi bi-trash\" style=\"padding-right: 10%;\"></i>"
            html+="Gráfica</a>"
            html+='</div>'
            html+='</div>'
            if not (self.finish):
                html+='<div style="display: flex; justify-content: center; align-items: center;height: '+str(self.row.high.value*0.90)+'em;">'
                html+='<span class="badge bg-soft-danger text-danger" style="font-size: 1em">ERROR, NO SE COMPLETO DE DETALLAR ESTA GRAFICA</span>'    
                html+='</div>'
            else:
                #Meter aqui la grafica
                #html+='<div id="id_'+str(self.id)+'" style="width: content-box; height: '+str(self.row.high.value*0.92)+'em; margin-top: '+str(self.row.high.value*0.03)+'em;"></div>'
                if (self.type_graph.id==5):
                    html+='<div id="id_'+str(self.id)+'_tab" style="width: content-box; height: '+str(self.row.high.value)+'em; margin-top: '+str(self.row.high.value*0.03)+'em;">'
                    html+=self.gettab(min, max)
                else:
                    #Meter aqui la card
                    html+='<div id="id_'+str(self.id)+'" style="width: content-box; height: '+str(self.row.high.value)+'em; margin-top: '+str(self.row.high.value*0.03)+'em;">'
                    if (self.type_graph.id==6):
                        html+=self.getcard(min, max)
                
                
            html+='</div>'
            html+='</div>'
            html+='</div>'

        html+='</div>'
        return "%s" % (html)


    def getGraph(self, min=None, max=None):
        variable=""
        if(self.type_graph.id==4):
            variable=""+str(self.getpie(min, max))
        elif(self.type_graph.id==2):
            variable=""+str(self.getbar(min, max))
        elif(self.type_graph.id==1):
            variable=""+str(self.getbar(min, max))
        elif(self.type_graph.id==3):
            variable=""+str(self.getbar(min, max))
        return variable

    def getpie(self, min=None, max=None):
        yrow=YRow.objects.filter(graph=self).first()
        API_V1_STR = os.environ.get('API_V1_STR')
        url=API_V1_STR+"pie"
        #_text='{"x": "'+self.xrow.name_db+'","y": {"value": "'+yrow.value.name_db+'","calculate": "'+yrow.type_calculate.value+'"},"dataset": "'+self.endpoint.name_db+'"}'
        #_json=json.loads(_text)
    
        #_json=self.send
        _json=self.send_json(min, max)
        token=""
        _headers={'Content-Type':'application/json', 'Autorization':token}
        response=requests.post(url, data=json.dumps(_json), headers=_headers)
        _json=json.loads(response.content)
        _json["series"][0]['type']= 'pie'
        _json["series"][0]['radius']= '50%'
        itemStyle={}
        itemStyle['shadowBlur']='10'
        itemStyle['shadowOffsetX']='0'
        itemStyle['shadowColor']='rgba(0, 0, 0, 0.5)'
        emphasis={}
        emphasis['itemStyle']=itemStyle
        _json["series"][0]['emphasis']= emphasis
        __temp=('{"title": {"text": "'+self.title+'", "subtext": "'+yrow.type_calculate.name+'", "left": "center" }, "tooltip": { "trigger": "item" }, "legend": { "orient": "vertical", "left": "left", "textStyle":{"width": "70","overflow":"truncate"} }, "toolbox": {"feature": {"saveAsImage": { } } } }')
        __final=json.loads(str(__temp))
        __final["series"]=_json["series"]
        return (str(__final).replace("'", "\""))



    def getbar(self, min=None, max=None):
        yrow=YRow.objects.filter(graph=self).first()
        API_V1_STR = os.environ.get('API_V1_STR')
        url=API_V1_STR+"line_bar"
        _json=self.send_json(min, max)
    
        token=""
        _headers={'Content-Type':'application/json', 'Autorization':token}
        response=requests.post(url, data=json.dumps(_json), headers=_headers)
        _json=json.loads(response.content)

        _json["xAxis"]['type']= 'category'
        _json["xAxis"]['boundaryGap']= 'true'
        if(self.type_graph.id==1):
            for element in _json["series"]:
                element["type"]='line'
        else:#(self.type_graph.id==2):
            for element in _json["series"]:
                element["type"]='bar'

        #Jonathan
        #__temp=('{"title": {"text": "'+self.title+'", "subtext": "'+yrow.type_calculate.name+'", "left": "center"}, "tooltip": { "trigger": "item" }, "legend": { "orient": "vertical", "top": "10%", "right": "right" ,"containLabel": "true", "textStyle":{"width": "70","overflow":"truncate"} },"dataZoom": [{"startValue": "'+ _json["xAxis"]["data"][0] +'"}, {"type": "inside"}], "grid": {"left": "3%","right": "15%","bottom": "18%", "top": "13%","containLabel": "true"},"toolbox": {"feature": {"saveAsImage": { },"dataZoom": {"yAxisIndex": "none"} } }, "yAxis": {"type": "value"} }')
        if (self.type_agrupation==1):
            if(self.type_graph.id==3):
                __temp=('{"title": {"text": "'+self.title+'", "subtext": "'+yrow.type_calculate.name+'", "left": "center"}, "tooltip": { "trigger": "item" }, "legend": { "orient": "vertical", "top": "10%", "right": "right" ,"containLabel": "true", "textStyle":{"width": "70","overflow":"truncate"} }, "grid": {"left": "3%","right": "15%","bottom": "18%", "top": "13%","containLabel": "true"},"toolbox": {"feature": {"saveAsImage": { },"dataZoom": {"xAxisIndex": "none"} } }, "yAxis": {"type": "value"} }')
            else:
                __temp=('{"title": {"text": "'+self.title+'", "subtext": "'+yrow.type_calculate.name+'", "left": "center"}, "tooltip": { "trigger": "item" }, "legend": { "orient": "vertical", "top": "10%", "right": "right" ,"containLabel": "true", "textStyle":{"width": "70","overflow":"truncate"} }, "grid": {"left": "3%","right": "15%","bottom": "18%", "top": "13%","containLabel": "true"},"toolbox": {"feature": {"saveAsImage": { },"dataZoom": {"yAxisIndex": "none"} } }, "yAxis": {"type": "value"} }')
        else:
            if(self.type_graph.id==3):
                __temp=('{"title": {"text": "'+self.title+'", "left": "center"}, "tooltip": { "trigger": "item" }, "legend": { "orient": "vertical", "top": "10%", "right": "right" ,"containLabel": "true", "textStyle":{"width": "70","overflow":"truncate"} }, "grid": {"left": "3%","right": "15%","bottom": "18%", "top": "13%","containLabel": "true"},"toolbox": {"feature": {"saveAsImage": { },"dataZoom": {"xAxisIndex": "none"} } }, "yAxis": {"type": "value"} }')
            else:
                __temp=('{"title": {"text": "'+self.title+'", "left": "center"}, "tooltip": { "trigger": "item" }, "legend": { "orient": "vertical", "top": "10%", "right": "right" ,"containLabel": "true", "textStyle":{"width": "70","overflow":"truncate"} }, "grid": {"left": "3%","right": "15%","bottom": "18%", "top": "13%","containLabel": "true"},"toolbox": {"feature": {"saveAsImage": { },"dataZoom": {"yAxisIndex": "none"} } }, "yAxis": {"type": "value"} }')

        __final=json.loads(str(__temp))
        __final["xAxis"]=_json["xAxis"]
        __final["series"]=_json["series"]

        
        if(self.type_graph.id==3):
            yAxis=__final["xAxis"]
            xAxis=__final["yAxis"]
            __final["yAxis"]=yAxis
            __final["xAxis"]=xAxis

        #Jonathan
        return str((str(__final).replace("'", "\"")).replace("None", "0"))




    def getcard(self, min=None, max=None):
        API_V1_STR = os.environ.get('API_V1_STR')
        url=API_V1_STR+"card"
        #_json=self.send
        _json=self.send_json(min, max)
        token=""
        _headers={'Content-Type':'application/json', 'Autorization':token}
        response=requests.post(url, data=json.dumps(_json), headers=_headers)
        _json=json.loads(response.content)
        if(self.type_icon):
            return '<div class="row"><div class="col-4"><div class="avatar-lg rounded-circle bg-'+self.type_icon.color+' border-'+self.type_icon.color+' border shadow" style="height: 3.5rem; width: 3.5rem;"><i class="'+self.type_icon.icon+' font-26 avatar-title text-white"></i></div></div><div class="col-8"><div class="text-end"><h3 class="text-dark mt-1"><span data-plugin="counterup">'+(str(float("{:.2f}".format(_json['data']))))+'</span></h3><p class="text-muted mb-1 text-truncate">'+self.title+'</p></div></div></div>'
        return '<div class="row"><div class="col-4"></div><div class="col-8"><div class="text-end"><h3 class="text-dark mt-1"><span data-plugin="counterup">'+(str(float("{:.2f}".format(_json['data']))))+'</span></h3><p class="text-muted mb-1 text-truncate">'+self.title+'</p></div></div></div>'

    def gettab(self, min=None, max=None):
        API_V1_STR = os.environ.get('API_V1_STR')
        url=API_V1_STR+"tab"
        #_json=self.send
        _json=self.send_json(min, max)
        token=""
        _headers={'Content-Type':'application/json', 'Autorization':token}
        response=requests.post(url, data=json.dumps(_json), headers=_headers)
        _json=json.loads(response.content)
        head=YRow.objects.filter(graph=self).order_by('id')
        data=_json['data']
        html='<h4 class="header-title" style="padding-bottom: 0.6em;">'+self.title+'</h4>'
        html+='<table id="'+self.name()+'" class="table dt-responsive nowrap w-100">'
        #html='<table id="datatable-buttons" class="table table-striped dt-responsive nowrap w-100">'

        
        
        html+='<thead>'
        html+='<tr>'
        for enc in head:
            html+='<th>'+enc.name+'</th>'
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
        
        return  html


class YRow (models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    graph=models.ForeignKey(Graph,  on_delete=models.CASCADE, related_name='Graph')
    value=models.ForeignKey(Detail,  on_delete=models.CASCADE, related_name='Detail_Y')
    type_calculate=models.ForeignKey(Type_calculate,  on_delete=models.CASCADE, null=True, related_name='Type_calculate')
    def __str__(self):
        return "%s" % (self.name)



class Graph_Filter(models.Model):
    id=models.AutoField(primary_key=True)
    comparate_value = models.CharField(max_length=400, null=True)
    value=models.ForeignKey(Detail,  on_delete=models.CASCADE, related_name='Value')
    graph=models.ForeignKey(Graph,  on_delete=models.CASCADE, related_name='Graph_Filter')
    filter=models.ForeignKey(Filter,  on_delete=models.CASCADE, related_name='Filter')
    type_comparation=models.ForeignKey(Type_comparation,  on_delete=models.CASCADE, related_name='Type_comparation', null=True)
    def __str__(self):
        return "%s" % (self.filter)