from django.shortcuts import render

from .forms import BusquedaInmuebleForm

#HTTDOCS
HTMLHOME = 'home.html'
HTMLLOGIN = 'login.html'

# Create your views here.
def home(request):
    data = {
        'form': BusquedaInmuebleForm()
    }
    
    return render(request, HTMLHOME, {**data})

def login(request):
    data = {
        
    }
    
    return render(request, HTMLLOGIN, {**data})