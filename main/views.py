from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import Inmueble, TipoDocumento, TipoUsuario, Usuario
from .forms import FiltrarInmuebles,CrearInmuebleForm, BusquedaInmuebleForm, LoginForm, RegisterForm, EditAccountBasics, EditAccountDangerZone
from django.contrib.auth import authenticate, login, logout

#Variables
USERLENGTHMIN = 4
PASSLENGTHMIN = 8

#HTTDOCS
HTMLHOME = 'home.html'
HTMLLOGIN = 'login.html'
HTMLUSERAREA = 'user_area.html'
HTMLUSEREDIT = 'user_edit.html'
HTMLCREARINMUEBLE = 'inmueble_crear.html'

#MENSAJES
SUCCESS_1 = "Guardado con éxito"

ERROR_1 = "El nombre de usuario ya existe."
ERROR_3 = "Error desconocido."
ERROR_2 = "Formulario inválido."
ERROR_4 = "Usuario o contraseña incorrecta."
ERROR_5 = "Usuario o documento demasiado corto(s)."
ERROR_6 = f"Nombre de usuario muy corto. Minimo {USERLENGTHMIN} caracteres"
ERROR_8 = "La contraseña anterior no es la correcta."
ERROR_9 = "Alguna(s) de las contraseñas no cumplen con la longitud minima."
ERROR_10 = "Las contraseñas nuevas no coinciden"
ERROR_11 = "Nombre o apellidos no cumplen con la longitud minima."

#Funcitions
#Decorador que valida que el usuario no esté logueado para hacer algo.
def unloginRequired(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
def home(request):
    data = {
        'form': BusquedaInmuebleForm()
    }
    
    return render(request, HTMLHOME, {**data})

@unloginRequired
def Login(request):
    data = {
        'LoginForm': LoginForm(),
        'RegisterForm': RegisterForm(),
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
                    data['error'] = ERROR_5
                    return render(request, HTMLLOGIN, {**data})        
                
                logedUser = authenticate(request, username=username, password=password)
                
                if logedUser is None:
                    data['LoginForm'] = LoginForm(initial={'username': username})
                    data['error'] = ERROR_4
                    return render(request, HTMLLOGIN, {**data})
    
                login(request, logedUser)
                
                #--Redirigir a area del usuario
                return redirect('userarea')
            else:
                data['error'] = ERROR_2
                return render(request, HTMLLOGIN, {**data})
            
        ##--------------REGISTRO----------------##
        elif 'register' in request.POST:    
            form = RegisterForm(request.POST)
            
            if form.has_error('username', code="unique"):
                data['error'] = ERROR_1
                data['RegisterForm'] = form
                return render(request, HTMLLOGIN, {**data})
            
            if form.is_valid():
                data['recycledRegisterForm'] = form
                try:
                    username_str = form.cleaned_data['username']
                    password_str = form.cleaned_data['password']
                    tipo_usuario_instancia = get_object_or_404(TipoUsuario, pk=0)

                    if len(username_str) < USERLENGTHMIN or len(password_str) < PASSLENGTHMIN:
                        data['error'] = ERROR_5
                        return render(request, HTMLLOGIN, {**data})
                    
                    user = form.save(commit=False)
                    user.username = username_str
                    user.set_password(password_str)
                    user.tipo_usuario = tipo_usuario_instancia
                    user.save()
                    
                    data['error'] = "Usuario creado con exito"
                    data['RegisterForm'] = RegisterForm()
                    return render(request, HTMLLOGIN, {**data})

                except Exception as e:
                    print(e)
                    data['error'] = ERROR_3
                    return render(request, HTMLLOGIN, {**data})
            else:
                data['error'] = ERROR_2
                return render(request, HTMLLOGIN, {**data})
    
        else:
            data['error'] = ERROR_3
            return render, HTMLLOGIN, {**data}
    #Get
    else:
        return render(request, HTMLLOGIN, {**data})
    
@login_required
def Logout(request):
    logout(request)
    return redirect(reverse('home'))

@login_required
def CrearInmueble(request):
    data = {'form': CrearInmuebleForm()}
    
    return render(request, HTMLCREARINMUEBLE, {**data})

@login_required
def UserArea(request):
    data = {'form': FiltrarInmuebles(),
            'event': ''}
    
    INMUEBLES_POR_PAGINA = 12
    inmuebles_usuario = Inmueble.objects.filter(duenio=request.user.id)
    form = FiltrarInmuebles(request.GET)
    
    if form.is_valid():
        id_inmueble = form.cleaned_data.get('id')
        tipo_inmueble = form.cleaned_data.get('tipo_inmueble')
        municipio = form.cleaned_data.get('municipio')
        
        if id_inmueble:
            inmuebles_usuario = inmuebles_usuario.filter(id=id_inmueble)
        
        if tipo_inmueble:
            inmuebles_usuario = inmuebles_usuario.filter(tipo_inmueble=tipo_inmueble)
    
        if municipio:
            inmuebles_usuario = inmuebles_usuario.filter(municipio_ubicacion=municipio)
            
    paginator = Paginator(inmuebles_usuario, INMUEBLES_POR_PAGINA)
    page_number = request.GET.get('page')
    
    try:
        inmuebles_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        inmuebles_paginados = paginator.page(1)
    except EmptyPage:
        inmuebles_paginados = paginator.page(paginator.num_pages)
        
    data['inmuebles'] = inmuebles_paginados
    
    if request.method == 'POST':
        pass

    return render(request, HTMLUSERAREA, {**data})

@login_required
def UserEdit(request):
    user = request.user
    data = {}
    
    if request.method == 'POST':
        if 'acc_data' in request.POST:
            form = EditAccountBasics(request.POST, instance=user)
            if form.is_valid():
                form.save()
                data['acc_data_event'] = SUCCESS_1
                data['acc_badge_bg'] = 'bg-success'
            else:
                data['acc_data_event'] = ERROR_2
                data['acc_badge_bg'] = 'bg-danger'
        elif 'username_data' in request.POST:
            nuevo_username = request.POST.get('username', '').strip()
            data['us_badge_bg'] = 'bg-danger'
            
            if len(nuevo_username) == 0:
                data['username_data_event'] = ERROR_6
            elif len(nuevo_username) < USERLENGTHMIN:
                data['username_data_event'] = ERROR_11     
            elif Usuario.objects.filter(username=nuevo_username).exists():
                data['username_data_event'] = ERROR_1
            else:
                usuario_actual = request.user
                usuario_actual.username = nuevo_username
                usuario_actual.save()
                data['us_badge_bg'] = 'bg-success'
                data['username_data_event'] = SUCCESS_1
                
        elif 'dz_data' in request.POST:
            form = EditAccountDangerZone(request.POST)
            if form.is_valid():
                if form.has_error("username", code="unique"):
                    data['evento'] = ERROR_1
                    return render(request, HTMLUSEREDIT, {**data})

                data['dz_badge_bg'] = 'bg-danger'
                password_old = form.cleaned_data['password_old']
                password = form.cleaned_data['password']
                password2 = form.cleaned_data['password2']
           
                if user.check_password(password_old):
                    if len(password) >= PASSLENGTHMIN or len(password2) >= PASSLENGTHMIN:
                        if password == password2:
                            user.set_password(password)
                            user.save()
                            data['dz_badge_bg'] = 'bg-success'
                            data['dz_data_event'] = SUCCESS_1
                        else:
                            data['dz_data_event'] = ERROR_10
                    else:
                        data['dz_data_event'] = ERROR_9
                else:
                    data['dz_data_event'] = ERROR_8
            else:
                data['dz_data_event'] = ERROR_2
                
    initial_danger_form = {'username': user.username}
    data['edit_account_basics'] = EditAccountBasics(instance=user)
    data['edit_account_dangerzone'] = EditAccountDangerZone(initial=initial_danger_form)
    return render(request, HTMLUSEREDIT, {**data})
        
