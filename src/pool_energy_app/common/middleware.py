from django.shortcuts import redirect
from datetime import datetime, timedelta
from pool_energy_app.users.models import Rol
from pool_energy_app.forms.models import Marketplace, MarketplaceConnector, Store
from pool_energy_app.forms.models import UserStore
from pool_energy_app.forms.models import Connector

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
                return redirect('/')
        else:
            if str(request.path).startswith('/accounts'):
                return None
            else:
                return redirect('/accounts/login/')
        #Comprueba si tiene rol o es nuevo
        if str(request.user) != 'AnonymousUser':
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
            print('-------')
            print(nTiendas)
            print('-------')
            if nTiendas == 0:#  (str(request.path).startswith('/accounts/logout/')):
                return redirect("/forms/newClient/")
            else:
                print('************** con tiendas ******************')
                lastStore = UserStore.objects.filter(user=nId).order_by('-id').values_list('store',flat=True)[0]
                print(lastStore)
                print('*********************************************')
                if nConnectors == 0:
                   return redirect("/forms/token/{}/buttons/".format(lastStore))
                else:
                    # lastConnector = Connector.objects.filter(user=nId).order_by('-id').values_list('id',flat=True)[0] -- ver que solo funcione con amazon
                    lastConnector = Connector.objects.filter(user=nId,social_application_id__in=[1]).order_by('-id').values_list('id',flat=True)[0]
                    print(lastConnector)
                    nMarketplace = MarketplaceConnector.objects.filter(connector_id=lastConnector).count()
                    print(nMarketplace)
                    print('*********************************************')
                    if nMarketplace == 0:
                        return redirect("/forms/marketplace/{}/".format(lastConnector))


            if not(request.user.is_superuser):
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
                        if str(request.path).startswith('/config'):
                            return redirect('/')
        #Comprueba si es admin