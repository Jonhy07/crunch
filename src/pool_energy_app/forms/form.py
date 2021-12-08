from django import forms
from django.forms import widgets
from .models import Network
from .models import SocialApplication
from .models import Connector
from .models import Client
from .models import Store
from .models import Item
from .models import LinioStore
from .models import MonthGoals
from .models import Action
from .models import ItemAction
from .models import UserStore
from .models import Homologation

from pool_energy_app.users.models import User
from django.forms import ModelChoiceField
from django.forms.widgets import SelectMultiple, TextInput
from django.forms import formset_factory
from django.forms import ModelForm
#from auditads.redis_connector.connection import redis_connection

class DateInput(forms.DateInput):
	input_type = 'date'

class NetworkModelForm(forms.ModelForm):
	class Meta:
		model = Network 
		fields = ['name', 'logo', 'color', 'group_name']

class ClientSendMail(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['email']
		widgets = {
			'email': forms.TextInput(attrs={'class': 'form-group col-md-6','type':'email'}),
		}

class SocialApplicationModelForm(forms.ModelForm):
	network = ModelChoiceField(queryset=Network.objects.all(),  empty_label='Please select a Network')
	class Meta:
		model = SocialApplication 
		fields = ['name', 'network', 'application_id', 'application_key', 'application_secret', 'developer_token', 'auth_uri', 'callback_uri', 'access_uri', 'network', 'permissions_uri', 'user_info_uri']

class ConnectorModelForm(forms.ModelForm):
	network = ModelChoiceField(queryset=Network.objects.all(),  empty_label='Please select an network')
	class Meta:
		model = Connector
		fields = ['social_application', 'name', 'access_token', 'refresh_token', 'expiration_date', 'nonauto']

class ClientModelForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['name', 'client_since', 'phone', 'email', 'birthday']
		widgets = {
			'client_since':DateInput(),
			'birthday':DateInput(),
		}

class ClientNew(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['name','owner_name']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
			'owner_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
		}

class StoreModelForm(forms.ModelForm):
	client = ModelChoiceField(queryset=Client.objects.all(),  empty_label='Please select a Customer')
	#network = ModelChoiceField(queryset=Network.objects.all(),  empty_label='Please select an network')
	class Meta:
		model = Store
		fields = ['client', 'name', 'blueprint', 'status']

class LinioStoreModelForm(forms.ModelForm):
	store = ModelChoiceField(queryset=Store.objects.filter(),  empty_label='Please select a store')
	class Meta:
		model = LinioStore
		fields = ['store', 'userid', 'api_key', 'url']

class MonthGoalsModelForm(forms.ModelForm):
	store = ModelChoiceField(queryset=Store.objects.filter(),  empty_label='Please select a store')
	class Meta:
		model = MonthGoals
		fields = ['store', 'mes', 'anio', 'fee', 'sales_goal', 'units_goal', 'ads_spend_limit']

class ActionModelForm(forms.ModelForm):
	class Meta:
		model = Action
		fields = ['name']

class CustomSelect(forms.Select):
    def __init__(self, attrs=None, choices=()):
        self.custom_attrs = {}
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        # setting the attributes here for the option
        if value in self.custom_attrs:
            option['attrs'].update({k: v for k, v in self.custom_attrs[value].items()})
        return option

class ItemModelForm(forms.ModelForm):
	# store = ModelChoiceField(queryset=Store.objects.all(),  empty_label='Please select a store',widget=CustomSelect(attrs={'class': 'form-select'}))
	store = ModelChoiceField(queryset=Store.objects.all(),  empty_label='Please select a store')
	class Meta:
		model = Item
		fields = ['store', 'ktp', 'sku', 'nombre', 'plataforma', 'status','costo','marketplace']

class ItemActionModelForm(forms.ModelForm):
	store = ModelChoiceField(queryset=Store.objects.filter(),  empty_label='Please select a store')
	item = ModelChoiceField(queryset=Item.objects.filter(),  empty_label='Please select an item')
	action = ModelChoiceField(queryset=Action.objects.filter(),  empty_label='Please select an action')
	#store = ModelChoiceField(queryset=Store.objects.filter(),  empty_label='Please select a store',widget=CustomSelect(attrs={'class': 'form-control'}))#
	#item = ModelChoiceField(queryset=Item.objects.filter(),  empty_label='Please select an item',widget=CustomSelect(attrs={'class': 'form-control','id':'item'}))
	#action = ModelChoiceField(queryset=Action.objects.filter(),  empty_label='Please select an action',widget=CustomSelect(attrs={'class': 'form-control'}))
	class Meta:
		model = ItemAction
		fields = ['store','item', 'action', 'comment']
		widgets = {
			'comment': forms.TextInput(attrs={'class': 'form-control'}),
		}

class UserStoreModelForm(forms.ModelForm):
	user = ModelChoiceField(queryset=User.objects.filter(),  empty_label='Please select an user')
	store = ModelChoiceField(queryset=Store.objects.filter(),  empty_label='Please select a store')
	class Meta:
		model = UserStore
		fields = ['user', 'store']

class HomologationModelForm(forms.ModelForm):
	#store1 = ModelChoiceField(queryset=Store.objects.filter(),  empty_label='Please select an store',widget=CustomSelect(attrs={'class': 'form-control'}))
	item1 = ModelChoiceField(queryset=Item.objects.filter(),  empty_label='Please select an item',widget=CustomSelect(attrs={'class': 'form-control','id':'item1'}))
	item2 = ModelChoiceField(queryset=Item.objects.filter(),  empty_label='Please select an item',widget=CustomSelect(attrs={'class': 'form-control','id':'item2'}))
	#store2 = ModelChoiceField(queryset=Store.objects.filter(),  empty_label='Please select an store',widget=CustomSelect(attrs={'class': 'form-control'}))
	class Meta:
		model = Homologation
		fields = ['item1','item2']