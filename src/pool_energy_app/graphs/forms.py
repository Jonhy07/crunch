from django import forms
from django.contrib.messages.api import error
from django.db import models
from django.db.models import fields
from django.forms import ModelChoiceField
from django.forms.fields import ChoiceField, FileField, IntegerField
from django.utils.regex_helper import Choice
from .models import Type_graph, Graph, Type_agrupation, Type_calculate, YRow, Type_time_agrupation, Graph_Filter
from pool_energy_app.endpoint.models import Access_rol_endpoint, Endpoint, Detail

class GraphForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.rows = kwargs.pop('rows')
        self.user = kwargs.pop('user')
        super(GraphForm, self).__init__(*args, **kwargs)
        self.fields['column']=IntegerField(label="Columns ("+str(self.rows)+" columns available)", max_value=self.rows, min_value=1, required=True)

        #self.fields['endpoint'] =ModelChoiceField(queryset=Endpoint.objects.filter(Access_rol_endpoint__rol=self.user.rol), empty_label='Please select a dataset.')
        self.fields['endpoint']=ModelChoiceField(queryset=Endpoint.objects.filter(id__in=Access_rol_endpoint.objects.filter(rol=self.user.rol).values_list('endpoint').all()), empty_label='Please select a dataset.')

    type_graph =ModelChoiceField(queryset=Type_graph.objects.all(), empty_label='Please select a type of chart.')
    class Meta:
        model = Graph
        fields=['title', 'column', 'type_graph', 'endpoint']


class PieForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.pop('endpoint')
        super(PieForm, self).__init__(*args, **kwargs)
        self.fields['xrow'] =ModelChoiceField(queryset=Detail.objects.filter(endpoint=self.endpoint.pk, type_detail=3), empty_label='Please select value.', label="Campo de Agrupacion")

    class Meta:
        model = Graph
        fields=['xrow']


class BarXForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.pop('endpoint')
        super(BarXForm, self).__init__(*args, **kwargs)
        self.fields['xrow'] =ModelChoiceField(queryset=Detail.objects.filter(endpoint=self.endpoint.pk, type_detail=4), empty_label='Please select value to group.', label="Seleccione la columna")

    type_agrupation =ModelChoiceField(queryset=Type_agrupation.objects.all(), empty_label='Please select a type agrupation of chart.')
    type_time_agrupation =ModelChoiceField(queryset=Type_time_agrupation.objects.all(), empty_label='Please select the temporality in which the data is grouped .')
    class Meta:
        model = Graph
        fields=['xrow', 'type_agrupation', 'type_time_agrupation',]


class YRowForm(forms.ModelForm):
    type_calculate=ModelChoiceField(queryset=Type_calculate.objects.all(), empty_label='Please select the type of calculation you want for the graph.')
    class Meta:
        model = YRow
        fields=['name', 'type_calculate',]


class TabTypeForm(forms.ModelForm):
    type_agrupation =ModelChoiceField(queryset=Type_agrupation.objects.all(), empty_label='Please select a type agrupation of chart.')
    class Meta:
        model = Graph
        fields=['type_agrupation']


class YRow2Form(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.pop('endpoint')
        super(YRow2Form, self).__init__(*args, **kwargs)
        self.fields['value'] =ModelChoiceField(queryset=Detail.objects.filter(endpoint=self.endpoint.pk), empty_label='Please select column.', label="Seleccione la columna")

    class Meta:
        model = YRow
        fields=['name', 'value',]