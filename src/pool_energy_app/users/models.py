from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

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

    def get_dashboars_count(self):
        import pool_energy_app.charts.models
        dashboards=pool_energy_app.charts.models.Dashboard.objects.filter(rol__lte=self.rol).exclude(Assigned_dashboard__user=self)
        return len(dashboards)

    #def save(self,*args,**kwargs):
     #   t=Rol(self.rol).duration
      #  d = timedelta(days=t)
       # if not self.id:
        #    self.expirate = datetime.now() + d
         #   super(User,self).save(*args,**kwargs)