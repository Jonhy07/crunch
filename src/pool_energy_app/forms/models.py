from django.db import models
from pool_energy_app.users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
# Create your models here.

class Network(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField()
    color = models.CharField(max_length=20, null=True)
    group_name = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.name)
    def get_update_url(self):
        return "/network/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/network/{}/delete".format(self.pk)

class Client(models.Model):
    name = models.CharField(max_length=100,verbose_name='Client Name')
    client_since = models.DateTimeField(null=True)
    owner_name = models.CharField(max_length=100,verbose_name='Store Name')
    owner_lastname = models.CharField(max_length=100)
    consultor = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birthday = models.DateTimeField(null=True)
    status = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.name)
    def get_update_url(self):
        return "/client/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/client/{}/delete".format(self.pk)

class Store(models.Model):
    Opcion1 = 'Activado'
    Opcion2 = 'Desactivado'
    Opciones = (
        (Opcion1, u"Activado"),
        (Opcion2, u"Desactivado")
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    blueprint = models.CharField(max_length=100)
    status= models.CharField(max_length=100,choices=Opciones)
    def __str__(self):
        return "%s" % (self.name)
    def get_buttons_url(self):
        return "/token/{}/buttons".format(self.pk)
    def get_liniostore_url(self):
        return "/liniostore/{}/list".format(self.pk)
    def get_update_url(self):
        return "/store/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/store/{}/delete".format(self.pk)
    def get_download_url(self):
        return"/store/{}/download".format(self.pk)

class Item(models.Model):
    Opcion1 = 'Activado'
    Opcion2 = 'Desactivado'
    Opciones = (
        (Opcion1, u"Activado"),
        (Opcion2, u"Desactivado")
    )
    store       = models.ForeignKey(Store, on_delete=models.CASCADE)
    plataforma  = models.CharField(max_length=100,null=True)
    ktp         = models.CharField(max_length=100,null=True)
    sku         = models.CharField(max_length=100,null=True)
    nombre      = models.CharField(max_length=600,null=True)
    marketplace = models.CharField(max_length=30,null=True)
    status      = models.CharField(max_length=100,choices=Opciones)
    costo       = models.FloatField(null=True)
    def __str__(self):
        return "%s" % (self.nombre)
    def get_update_url(self):
        return "/item/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/item/{}/delete".format(self.pk)

class Item_temp(models.Model):
    store 		= models.PositiveSmallIntegerField()
    plataforma 	= models.CharField(max_length=100,null=True)
    ktp 		= models.CharField(max_length=100,null=True)
    sku 		= models.CharField(max_length=100,null=True)
    nombre 		= models.CharField(max_length=600,null=True)
    marketplace = models.CharField(max_length=30,null=True)
    status 		= models.CharField(max_length=100,null=True)

class LinioStore(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    userid = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.userid)
    def get_update_url(self):
        return "/liniostore/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/liniostore/{}/delete".format(self.pk)

class SocialApplication(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    application_id = models.CharField(max_length=200, null=True)
    application_key = models.CharField(max_length=200)
    application_secret = models.CharField(max_length=200)
    developer_token = models.CharField(max_length=200)
    auth_uri = models.CharField(max_length=200)
    callback_uri = models.CharField(max_length=200)
    access_uri = models.CharField(max_length=200)
    permissions_uri = models.CharField(max_length=200)
    user_info_uri = models.CharField(max_length=200, null=True)
    def __str__(self):
        return "%s" % (self.name)
    def get_update_url(self):
        return "/socialapplication/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/socialapplication/{}/delete".format(self.pk)

class SocialApplicationPermission(models.Model):
    social_application = models.ForeignKey(SocialApplication, on_delete=models.CASCADE)
    permission = models.CharField(max_length=100)
    separator = models.CharField(max_length=10, null=True)
    def _str_(self):
        return self.permission
    def get_update_url(self):
        return "/socialapplication_permission/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/socialapplication_permission/{}/delete".format(self.pk)

class Connector(models.Model):
    social_application = models.ForeignKey(SocialApplication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=600)
    access_token = models.CharField(max_length=600, null=True)
    refresh_token = models.CharField(max_length=600, null=True)
    expiration_date = models.DateTimeField(null=True)
    nonauto = models.BooleanField(null=True)
    customer_id = models.CharField(max_length=600, null=True)
    def __str__(self):
        return "%s" % (self.name)
    def get_update_url(self):
        return "/connector/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/connector/{}/delete".format(self.pk)

class StoreConnector(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE)
    def __str__(self):
        return self.connector.name +'-'+ self.stores.name
    def get_update_url(self):
        return "/storeconnector/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/storeconnector/{}/delete".format(self.pk)

class Marketplace(models.Model):
    country = models.CharField(max_length=100)
    marketplace_id = models.CharField(max_length=100)
    country_code = models.CharField(max_length=4)
    logo = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.country)

class MarketplaceConnector(models.Model):
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE)
    def __str__(self):
        return self.marketplace.country +'-'+ self.connector.name

class MonthGoals(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    mes = models.PositiveSmallIntegerField()
    anio = models.PositiveSmallIntegerField()
    fee = models.FloatField()
    sales_goal = models.FloatField()
    units_goal = models.FloatField()
    ads_spend_limit = models.FloatField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store', 'mes', 'anio'], name='UC_StoreMesAnio_MonthGoals')
        ]
    
    def __str__(self):
        return "%s" % (self.userid)
    def get_update_url(self):
        return "/monthgoals/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/monthgoals/{}/delete".format(self.pk)

class Action(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.name)
    def get_update_url(self):
        return "/action/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/action/{}/delete".format(self.pk)

class ItemAction(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, null=True)
    ktp = models.CharField(max_length=100, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    creation_date= models.DateTimeField(auto_now_add=True, blank=True)
    comment = models.CharField(max_length=100)
    def __str__(self):
        return self.item.nombre +'-'+ self.action.name
    def get_update_url(self):
        return "/itemaction/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/itemaction/{}/delete".format(self.pk)

class UserStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name +'-'+ self.store.name
    def get_update_url(self):
        return "/userstore/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/userstore/{}/delete".format(self.pk)

class Homologation(models.Model):
    item1 = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='item1')
    item2 = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='item2')
    def __str__(self):
        return self.item1.nombre + '-' + self.item2.nombre
    def get_update_url(self):
        return "/homologation/{}/change".format(self.pk)
    def get_delete_url(self):
        return"/homologation/{}/delete".format(self.pk)