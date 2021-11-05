from django.db import models
from pool_energy_app.users.models import Rol, User

class Dashboard(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Dashboards')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='Rol_Dashboard', null=True)
    def __str__(self):
        return "%s" % (self.name)
    def get_update_url(self):
        return "/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/{}/delete".format(self.pk)
    def to_html(self, min=None, max=None,Tienda=None):
        html=''
        row=Row.objects.filter(dashboard=self).order_by('id')
        for object in row:
            html+="<br><div class=\"row\">"
            html+=object.to_html(min, max,Tienda)
            html+="</div>"
        return "%s" % (html)
    def names(self):
        row=Row.objects.filter(dashboard=self).order_by('id')
        name=[]
        for object in row:
            name.extend(object.names())
        return name

    def options(self, min=None, max=None,Tienda=None):
        row=Row.objects.filter(dashboard=self).order_by('id')
        option=[]
        for object in row:
            option.extend(object.options(min, max,Tienda))
        return option

    def tables(self):
        row=Row.objects.filter(dashboard=self).order_by('id')
        tab=[]
        for object in row:
            tab.extend(object.tables())
        return tab

    def sizes(self):
        row=Row.objects.filter(dashboard=self).order_by('id')
        tab=[]
        for object in row:
            tab.extend(object.sizes())
        return tab

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['user', 'name'], name='dashuser')
            ]

class Column(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    columns = models.IntegerField(null=False)
    value = models.IntegerField(null=False)
    def __str__(self):
        return "%s" % (self.name)

class High(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    value = models.IntegerField(null=False)
    def __str__(self):
        return "%s" % (self.name)

class Row(models.Model):
    id=models.AutoField(primary_key=True)
    available  = models.IntegerField(null=False)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='Dashboards')
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='Column')
    high = models.ForeignKey(High, on_delete=models.CASCADE, related_name='High')
    def __str__(self):
        return "%s" % (self.id)
    def get_update_url(self):
        return "/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/row/{}/delete".format(self.pk)
    def get_add_graph_url(self):
        return"/row/graph/{}/new".format(self.pk)

    def names(self):
        name=[]
        import pool_energy_app.graphs.models
        graphs=pool_energy_app.graphs.models.Graph.objects.filter(row=self.id).order_by('id')
        for object in graphs:
            if(object.type_graph.id>0 and object.type_graph.id<5):
                if(object.finish):
                    name.append(object.name())
        return name

    def tables(self):
        tab=[]
        import pool_energy_app.graphs.models
        graphs=pool_energy_app.graphs.models.Graph.objects.filter(row=self.id).order_by('id')
        for object in graphs:
            if(object.type_graph.id==5):
                if(object.finish):
                    tab.append(object.name())
        return tab

    def sizes(self):
        tab=[]
        import pool_energy_app.graphs.models
        graphs=pool_energy_app.graphs.models.Graph.objects.filter(row=self.id).order_by('id')
        for object in graphs:
            if(object.type_graph.id==5):
                if(object.finish):
                    #tab.append(object.row.high.value*0.54)
                    tab.append((object.row.high.value-16.5))
        return tab

    def options(self, min=None, max=None,Tienda=None):
        option=[]
        import pool_energy_app.graphs.models
        graphs=pool_energy_app.graphs.models.Graph.objects.filter(row=self.id).order_by('id')
        for object in graphs:
            if(object.type_graph.id>0 and object.type_graph.id<5):
                if(object.finish):
                    option.append(object.getGraph(min, max,Tienda))
        return option

    def to_html(self, min=None, max=None,Tienda=None):
        html=''

        #Pintar Graficas
        import pool_energy_app.graphs.models
        graphs=pool_energy_app.graphs.models.Graph.objects.filter(row=self.id).order_by('id')
        html+="<div class=\"col\">"
        html+="<div class=\"row\">"
        for object in graphs:
            html+=object.to_html(min, max,Tienda)
        #Pintar Vacios
        if (self.available>0):
            for i in range(self.available):
                html+="<div class=\"col-"+str (self.column.value)+"\" style=\"height: "+str(self.high.value)+"em;\">"
                html+="</div>"
            html+="</div>"
            html+="</div>"

            html+="<div class=\"col-1 toolsrow hideme\" style=\"height: "+str(self.high.value)+"em;\">"
            html+="<a  class=\"dropdown-item notify-item delete\" title=\"Eliminar Fila\" href=\"/dashboard"+self.get_delete_url()+"\"  onclick=\"return confirm('Esta accion borrara todas las graficas asociadas a la fila')\">"
            html+="<i class=\"bi bi-trash\" style=\"padding-right: 10%;\"></i>"
            html+="Fila</a>"
            html+="<a  class=\"dropdown-item notify-item delete\" title=\"Agregar Grafico\" href=\"/dashboard"+self.get_add_graph_url()+"\">"
            html+="<i class=\"bi bi-plus-lg\" style=\"padding-right: 10%;\"></i>"
            html+="Gráfico</a>"
            html+="</div>"
        else:
            html+="</div>"
            html+="</div>"

            html+="<div class=\"col-1 toolsrow hideme\" style=\"height: "+str(self.high.value)+"em;\">"
            html+="<a  class=\"dropdown-item notify-item delete\" title=\"Eliminar Fila\" href=\"/dashboard"+self.get_delete_url()+"\"  onclick=\"return confirm('Esta accion borrara todas las graficas asociadas a la fila')\">"
            html+="<i class=\"bi bi-trash\" style=\"padding-right: 10%;\"></i>"
            html+="Fila</a>"
            html+="</div>"
        return "%s" % (html)

class User_Dashboard(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Assigned_user')
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='Assigned_dashboard')
    edit  = models.IntegerField(null=False)
    delete  = models.IntegerField(null=False)