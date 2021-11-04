from django.shortcuts import render

# Create your views here.

#Vista tiempo expirado
def expired(request):
    context = {
    }
    return render(request, "errors/expired.html", context)
