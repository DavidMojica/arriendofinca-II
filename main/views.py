from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import BusquedaInmuebleForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout

#Variables
USERLENGTHMIN = 4
PASSLENGTHMIN = 8

#HTTDOCS
HTMLHOME = 'home.html'
HTMLLOGIN = 'login.html'

#MENSAJES
ERROR_1 = "El nombre de usuario ya existe."
ERROR_3 = "Error desconocido."
ERROR_2 = "Formulario inválido."
ERROR_4 = "Usuario o contraseña incorrecta."
ERROR_6 = "Usuario o documento demasiado corto(s)."

#Funcitions
#Decorador que valida que el usuario no esté logueado para hacer algo.
def unloginRequired(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('orders')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
def home(request):
    data = {
        'form': BusquedaInmuebleForm()
    }
    
    return render(request, HTMLHOME, {**data})

def login(request):
    data = {
        'LoginForm': LoginForm(),
        'RegisterForm': RegisterForm()
    }

    if request.method == 'POST':
        if 'login' in request.POST:
            form = LoginForm(request.POST)
            print(form)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                if len(username) < USERLENGTHMIN or len(password) < PASSLENGTHMIN:
                    data['LoginForm'] = LoginForm(initial={'username': username})
                    data['error'] = ERROR_6
                    return render(request, HTMLLOGIN, {**data})        
                
                logedUser = authenticate(request, username=username, password=password)

                print(logedUser)
                if logedUser is None:
                    data['LoginForm'] = LoginForm(initial={'username': username})
                    data['error'] = ERROR_6
                    return render(request, HTMLLOGIN, {**data})
    
                login(request, logedUser)
            else:
                data['error'] = ERROR_2
                return render(request, HTMLLOGIN, {**data})
        elif 'register' in request.POST:    
            form = RegisterForm(request.POST)
            if form.is_valid():
                data['recycledRegisterForm'] = form


                if form.has_error('username', code="unique"):
                    data['error'] = ERROR_1
                    return render(request, HTMLLOGIN, {**data})

                try:
                    event = None
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    tipo_usuario = 0

                    if len(username) < USERLENGTHMIN or len(password) < PASSLENGTHMIN:
                        data['error'] = ERROR_6
                        return render(request, HTMLLOGIN, {**data})
                    
                    user = form.save(commit=False)
                    user.username = username
                    user.set_password(password)
                    user.email = form.cleaned_data['email']

                except Exception as e:
                    data['error'] = ERROR_3
                    return render(request, HTMLLOGIN, {**data})
    #Get
    else:
        return render(request, HTMLLOGIN, {**data})
    
@login_required
def Logout(request):
    logout(request)
    return redirect(reverse('home'))