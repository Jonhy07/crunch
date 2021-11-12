from django.shortcuts import redirect
from datetime import datetime, timedelta
from pool_energy_app.users.models import Rol
from pool_energy_app.forms.models import Marketplace, MarketplaceConnector, Store
from pool_energy_app.forms.models import UserStore
from pool_energy_app.forms.models import Connector
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponseRedirect

class UsersPermissions():
    def __init__(self, get_response):
        self.get_response=get_response

    def __call__(self, request):
        #if str(request.user) != 'AnonymousUser' :
        response=self.get_response(request)
        return response

    #Se ejecuta antes y despues 
    def process_view(self, request, view_fun, view_args, view_kwargs):
        #Comprueba si no es un usuario anonimo para redirects
        if str(request.user) != 'AnonymousUser' :
            if str(request.path).startswith('/accounts/login'):
                print('redirigiendo')
                return redirect('/')
        else:
            if str(request.path).startswith('/accounts'):
                return None
            else:
                return redirect('/accounts/login/')

        if str(request.user) != 'AnonymousUser':
           #  lConnectors = .objects.filter(user__pk=nId).values_list('id',flat=True)
            grupo = Group.objects.filter(id=request.user.rol_id).values_list('id',flat=True)
            perm_tuple_all = Permission.objects.filter(group__id=grupo[0]).values_list('codename',flat=True)
            perm_tuple_type_id = list(Permission.objects.filter(group__id=grupo[0]).values_list('content_type_id',flat=True))
            print('******************************')
            print('******************************')
            print(request.user.rol.get_rol)
            print('----')
            perm_tuple=[]
            j=0
            for i in perm_tuple_type_id:
                perm_tuple_type = list(ContentType.objects.filter(id=i).values_list('app_label',flat=True))
                perm_tuple.append(perm_tuple_type[0]+ '.'+perm_tuple_all[j])
                j+=1
            print(perm_tuple)
            sep_path=request.path.split('/')
            if str(request.path).startswith('/accounts'):
                return None
            elif str(request.path).startswith('/oauth'):
                return None
            elif str(request.path) == '/403/':
                return None
            elif (request.user.rol_id != 4):
                #pendiente de incluir la conexión aouth
                nId=request.user.id
                lConnectors = Connector.objects.filter(user__pk=nId).values_list('id',flat=True)
                nConnectors = Connector.objects.filter(user__pk=nId).count()
                if nConnectors > 0:
                    nMarketplace = MarketplaceConnector.objects.filter(connector__in=list(lConnectors)).count()
                else:
                    nMarketplace=0
                if str(request.path).startswith('/forms/newClient/'):
                    return None
                if str(request.path).startswith('/forms/token/'):
                    return None
                if str(request.path).startswith('/forms/marketplace/'):
                    return None
                stores = UserStore.objects.filter(user=nId).values_list('store',flat=True)
                nTiendas = Store.objects.filter(pk__in=[stores]).count()
                if nTiendas == 0:
                    return redirect("/forms/newClient/")
                else:
                    lastStore = UserStore.objects.filter(user=nId).order_by('-id').values_list('store',flat=True)[0]
                    if nConnectors == 0:
                        return redirect("/forms/token/{}/buttons/".format(lastStore))
                    else:
                        lastConnector = Connector.objects.filter(user=nId,social_application_id__in=[1]).order_by('-id').values_list('id',flat=True)
                        if (lastConnector.count()>0):
                            nMarketplace = MarketplaceConnector.objects.filter(connector_id=list(lastConnector)[0]).count()
                            if nMarketplace == 0:
                                return redirect("/forms/marketplace/{}/".format(list(lastConnector)[0]))
                            else:
                                print('redirigiendo')
                                return None
            elif not(request.user.is_superuser):
                #No tiene rol le asigna uno
                if (request.user.rol.id==0):
                    rol=Rol.objects.filter(id=1).first()
                    d = timedelta(days=rol.duration)
                    request.user.expirate = datetime.now() + d
                    request.user.rol=rol
                    request.user.save()
                #Si tiene rol Verifica la expiracion
                else:
                    #verifica la fecha
                    if(request.user.expirate<datetime.now()):
                        if str(request.path).startswith('/expired'):
                            return None
                        if str(request.path).startswith('/accounts/logout/'):
                            return None
                        return redirect('/expired/')
                    else:
                        #impide el acceso a expired a los que no han expirado
                        if str(request.path).startswith('/expired'):
                            return redirect('/')
                        elif str(request.path).startswith('/config'):
                            return redirect('/')
                        elif str(request.path) == '/403/':
                            return None
            else:
                return None

            #prueba = Group.objects.all().values_list('id', flat=True)
            print(sep_path)
            j=0
            for i in sep_path:
                sep_path[j]= i.replace('social_application','socialapplication')
                j+=1
            if len(sep_path) >= 4:
                new_route=sep_path[1]+'.'+sep_path[4]+'_'+sep_path[2]
            elif len(sep_path) >= 3:
                sep_path[2]=sep_path[2].replace('list','view')
                sep_path[2]=sep_path[2].replace('create','add')
                new_route=sep_path[1]+'.'+sep_path[2]
            else:
                new_route=''
                return None
            print(new_route)
            print('******************************')
            print('******************************')
            if new_route in perm_tuple:
                return None
            elif str(request.path).startswith('/dashboard'):
                return None
            elif (str(request.path)=='forms.cargarStore_homologation' or str(request.path)=='forms.cargar2_homologation'):
                return None
            elif (str(request.path)=='forms.cargarStore_itemaction'):
                return None
            elif (str(request.path)=='forms.download_store'):
                return None
            else:
                print('no tiene permisos para ver esto... ')
                return redirect('/403/')

            # perm_tuple = request.user.get_group_permissions()
            # sep_path=request.path.split('/')
            # if sep_path[3] == 'list':
            #     path = sep_path[1]+'.view_'+sep_path[2]
            # elif sep_path[3].isnumeric():
            #     msg = 'number'
            #     path = sep_path[1]+'.'+sep_path[4]+'_'+sep_path[2]						
            # else:
            #     path = sep_path[1]+'.'+sep_path[3]+'_'+sep_path[2]

            # if str(path) in perm_tuple:
            #     return None
            # elif str(path) =='oauth.buttons_token' and (request.user.groups.filter(name='StoreOwner').exists() or request.user.groups.filter(name='Administrator').exists()):
            #     return None
            # elif (str(path) =='oauth.resp_token') and (request.user.groups.filter(name='StoreOwner').exists() or request.user.groups.filter(name='Administrator').exists()):
            #     return None
            # elif (str(path) =='oauth.view_marketplace' or str(path)== 'oauth.view_token') and (request.user.groups.filter(name='StoreOwner').exists() or request.user.groups.filter(name='Administrator').exists()):
            #     return None
            # elif (str(path)=='forms.cargarStore_homologation' or str(path)=='forms.cargar2_homologation'):
            #     return None
            # elif (str(path)=='forms.cargarStore_itemaction'):
            #     return None
            # elif (str(path)=='forms.download_store'):
            #     return None
            # else:
            #     print(str(path))
            #     print('no tiene permisos para ver esto... ')
            #     return redirect('/403/')

