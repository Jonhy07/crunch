import django_filters
from .models import *
from django_filters import DateFilter

class ItemFilter(django_filters.FilterSet):
	class Meta:
		model=Item
		fields= '__all__'
		exclude=['sku','status','plataforma','nombre','costo','marketplace']