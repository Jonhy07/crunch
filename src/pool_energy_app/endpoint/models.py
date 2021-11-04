from django.db import models
from pool_energy_app.users.models import Rol

# Create your models here.

class Endpoint (models.Model):
    id=models.AutoField(primary_key=True)
    name_db = models.CharField(max_length=250)
    name_bc = models.CharField(max_length=250)
    def __str__(self):
        return "%s" % (self.name_bc)


class Type_detail (models.Model):
    id=models.AutoField(primary_key=True)
    type = models.CharField(max_length=250)
    def __str__(self):
        return "%s" % (self.type)


class Detail (models.Model):
    id=models.AutoField(primary_key=True)
    name_db = models.CharField(max_length=250)
    name_bc = models.CharField(max_length=250)
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name='Endpoint_Detail')
    type_detail = models.ForeignKey(Type_detail, on_delete=models.CASCADE, related_name='Type_detail')
    def __str__(self):
        return "%s" % (self.name_bc)


class Access_rol_endpoint(models.Model):
    id=models.AutoField(primary_key=True)
    description= models.CharField(max_length=250)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='Rol_Access')
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name='Endpoint_Access')
    def __str__(self):
        return " %s tiene acceso a: %s" % (self.rol, self.endpoint)

