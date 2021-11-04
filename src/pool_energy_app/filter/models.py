from django.db import models
from pool_energy_app.endpoint.models import Type_detail


class Type_filter(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Type_comparation(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    signo = models.CharField(max_length=10)
    def __str__(self):
        return "%s" % (self.name)



class Filter(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    detail = models.CharField(max_length=400, null=True)
    type_filter=models.ForeignKey(Type_filter, on_delete=models.CASCADE, related_name='Type_filter_1')
    type_detail=models.ForeignKey(Type_detail, on_delete=models.CASCADE, related_name='Type_detail_1')
    def __str__(self):
        return "%s" % (self.name)
    
