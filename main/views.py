from django.shortcuts import render

from .forms import BusquedaInmuebleForm

# Create your views here.
def home(request):
    data = {
        'form': BusquedaInmuebleForm()
    }
    
    return render(request, 'home.html', {**data})