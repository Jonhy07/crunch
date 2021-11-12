from datetime import date, datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from pool_energy_app.charts.models import Dashboard
from pool_energy_app.common.views import expired
from pool_energy_app.users.models import Rol, User

def users(request):
    buscarpor = int(request.GET.get ('rol', "0"))
    usuarios=None
    if (buscarpor>0):
        usuarios=User.objects.filter(rol=buscarpor)
    else:
        usuarios=User.objects.all()
    context = {
        'usuarios' :usuarios
    }
    return render(request, "admin/listusers.html", context)


def usereditindex(request):
    id_user = int(request.GET.get ('user', "0"))
    if id_user==0:
        return redirect('/')
    usuario=User.objects.filter(id=id_user).first()

    roles=Rol.objects.filter(id__gt=0)
    context = {
        'usuario' :usuario,
        'roles': roles,
    }
    return render(request, "admin/edituser.html", context)

def update_user(request):
    id_user=int(request.POST["id_usuario"])
    id_rol=int(request.POST["id_rol"])
    expirate=(request.POST["expirate"])
    user=User.objects.filter(id=id_user).first()
    rol=Rol.objects.filter(id=id_rol).first()
    user.rol=rol
    user.expirate=expirate
    user.save()
    messages.success(request, "usuario Modificado Correctamente.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def list_dashboards(request):
    dashboards=Dashboard.objects.all()
    roles=Rol.objects.filter(id__gt=0).filter(id__lt=4)
    context = {
        'dashboards' :dashboards,
        'bandera_rol': 1,
        'roles': roles,
    }
    return render(request, "admin/listdashboards.html", context)