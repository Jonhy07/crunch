from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password

class Rol(models.Model):
    id=models.AutoField(primary_key=True)
    rol=models.CharField('Rol', max_length=50, unique=True)
    duration=models.IntegerField(default=0)
    create=models.IntegerField(default=0,null=True)

    class Meta:
        verbose_name= 'Rol'
        verbose_name_plural= 'Roles'

    def __str__(self):
        return self.rol
    def get_rol(self):
        return str (self.rol)
    def get_create(self):
        return int (self.create)

class User (AbstractUser):
    rol=models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True, default=0)
    expirate=models.DateTimeField(default=datetime.now())
    # name=models.CharField(blank=True, max_length=255, verbose_name="Name of User")
    def get_dashboars(self):
        import pool_energy_app.charts.models
        dashboards=pool_energy_app.charts.models.Dashboard.objects.filter(rol__lte=self.rol)
        return dashboards
    def get_permissions(self):
        grupo = Group.objects.filter(id=self.rol_id).values_list('id',flat=True)
        perm_tuple_all = Permission.objects.filter(group__id=grupo[0]).values_list('codename',flat=True)
        perm_tuple_type_id = list(Permission.objects.filter(group__id=grupo[0]).values_list('content_type_id',flat=True))
        perm_tuple=[]
        j=0
        for i in perm_tuple_type_id:
            perm_tuple_type = list(ContentType.objects.filter(id=i).values_list('app_label',flat=True))
            perm_tuple.append(perm_tuple_type[0]+ '.'+perm_tuple_all[j])
            j+=1
        return list(perm_tuple)
    def get_dashboars_count(self):
        import pool_energy_app.charts.models
        dashboards=pool_energy_app.charts.models.Dashboard.objects.filter(rol__lte=self.rol).exclude(Assigned_dashboard__user=self)
        return len(dashboards)

    def save(self,*args,**kwargs):
        if not self.id:
            if 'argon2$argon2i' not in self.password:
               self.password=make_password(self.password)
            super(User,self).save(*args,**kwargs)