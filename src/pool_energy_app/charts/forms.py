from django import forms
from django.forms import ModelChoiceField
from .models import Dashboard, Row, Column, High

class DashboardForm(forms.ModelForm):
	class Meta:
		model = Dashboard 
		fields = ['name', 'description']

class RowForm(forms.ModelForm):
	column = ModelChoiceField(queryset=Column.objects.all(),  empty_label='Please select the number of columns in the row.')
	high = ModelChoiceField(queryset=High.objects.all(),  empty_label='Please select a height for the columns.')
	class Meta:
		model= Row
		fields= ['column', 'high']