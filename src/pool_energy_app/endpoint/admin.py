from django.contrib import admin
from .models import Endpoint, Type_detail, Detail, Access_rol_endpoint


# Register your models here.
admin.site.register(Endpoint)
admin.site.register(Type_detail)
admin.site.register(Detail)
admin.site.register(Access_rol_endpoint)