from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import Inmueble, Municipio, TipoDocumento, TipoUsuario, Usuario, Imagenes
from .forms import FiltrarInmuebles,CrearInmuebleForm, BusquedaInmuebleForm, LoginForm, RegisterForm, EditAccountBasics, EditAccountDangerZone
from django.contrib.auth import authenticate, login, logout

#--Variables--#
USERLENGTHMIN = 4
PASSLENGTHMIN = 8

#-Imagenes de inmueble-#
MAX_IMAGE_MB = 2 #MB
MAX_IMAGES_PER_POST = 5 #Máximo de imágenes por inmueble

#--HTTDOCS--#
HTMLHOME = 'home.html'
HTMLLOGIN = 'login.html'
HTMLUSERAREA = 'user_area.html'
HTMLUSEREDIT = 'user_edit.html'
HTMLCREARINMUEBLE = 'inmueble_crear.html'

#--MENSAJES--#
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
ERROR_12 = f"Se excedió la cantida de imágenes. Maximo {MAX_IMAGES_PER_POST} imágenes."
ERROR_13 = f"Alguna imagen excede el peso permitido. Máximo {MAX_IMAGE_MB} Mb por imágen"
ERROR_14 = "Algún archivo cargado NO es una imagen."

#-----------------------------------------------------------------------------------------#
#-------------------------------------DECORADORES-----------------------------------------#
#-----------------------------------------------------------------------------------------#
def unloginRequired(view_func):
    """
    El usuario no puede tener la sesion iniciada para poder acceder a las funciones de una vista.
    Author: DavidMojica (Github)
    Usage: @unloginRequired sobre la vista.
    Args:
        view_func (ViewController): Vista controlada
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

#-----------------------------------------------------------------------------------------#
#----------------------------------------FUNCIONES----------------------------------------#
#-----------------------------------------------------------------------------------------#
@login_required
def Logout(request):
    """
    Cierra la sesión a un usuario logueado. No devuelve vista, redirige.
    Args:
        request (HttpRequest): Petición de http realizada por el usuario.
    Returns:
        Redirect: Redirecciona al home.
    """
    logout(request)
    return redirect(reverse('home'))

#-----------------------------------------------------------------------------------------#
#-----------------------------------------VISTAS------------------------------------------#
#-----------------------------------------------------------------------------------------#
#--HOME o Index--#
def home(request):
    data = { 'form': BusquedaInmuebleForm() }
    return render(request, HTMLHOME, {**data})

#--Inicio de sesión - Registro--#
@unloginRequired
def Login(request):
    """
    Vista de login/register
    Args:
        request (HttpRequest): Petición de http realizada por el usuario.
    Returns:
        HttpResponse: Renderizado gráfico de documento HTML con datos desde el servidor.
    """
    #--Variables--#
    data = {
        'LoginForm': LoginForm(),
        'RegisterForm': RegisterForm(),
    }

    #--Procesamiento de petición--#
    if request.method == 'POST':
        #--Procesamiento de formularios--#
        ##---------------LOGIN---------------##
        if 'login' in request.POST:
            form = LoginForm(request.POST)
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
                
                return redirect('userarea') #--Redirigir a area del usuario si se verifica la autenticidad del usuario --#
            else:
                data['error'] = ERROR_2 #--No redirigir y devolver mensaje de error--#
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
                    data['error'] = ERROR_3
                    return render(request, HTMLLOGIN, {**data})
            else:
                data['error'] = ERROR_2
                return render(request, HTMLLOGIN, {**data})
    
        else:
            data['error'] = ERROR_3
            return render(request, HTMLLOGIN, {**data})
    #Get
    else:
        return render(request, HTMLLOGIN, {**data})

#--Área del usuario--#
@login_required
def UserArea(request):
    """
    Vista que muestra ordenadamente los inmuebles del usuario. Desdea qui se puede añadir, modificar y borrar datos de los inmuebles.
    Después de iniciar sesion, se redirige automáticamente a esta vista.
    Args:
        request (HttpRequest): Petición de http realizada por el usuario.
    Returns:
        HttpResponse: Renderizado gráfico de documento HTML con datos desde el servidor.
    """
    
    #--Variables--#
    INMUEBLES_POR_PAGINA = 12
    data = {'form': FiltrarInmuebles(),
            'event': ''}
    inmuebles_usuario = Inmueble.objects.filter(duenio=request.user.id)
    form = FiltrarInmuebles(request.GET) #Si el formulario fue enviado por metodo get.
    
    #--Procesamiento de formularios--#
    if form.is_valid():
        #--Form de filtro--#
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
        pass #Aún no se le ha dado ninguna implementación a POST.

    return render(request, HTMLUSERAREA, {**data})

#--Controles para usuarios--#
@login_required
def CrearInmueble(request):
    """
    Vista de creación de un inmueble. Puede ser accedido por cualquier tipo de usuario.
    Args:
        request (HttpRequest): Petición de http realizada por el usuario.
    Returns:
        HttpResponse: Renderizado gráfico de documento HTML con datos desde el servidor.
    """
    #--Variables---#
    data = { 'form': CrearInmuebleForm(),
             'event': ''}
    
    #---Procesamiento de petición---#
    if request.method == 'POST':
        #--Procesamiento de formularios--#
        ##-------------Crear inmueble------------##
        if 'agregar_inmueble' in request.POST:
            form = CrearInmuebleForm(request.POST)
            ban_images = True
            
            #--Procesar elementos de un select fetcheado asincrónicamente--#
            municipio = request.POST.get('municipio_ubicacion')
            form.fields['municipio_ubicacion'].choices = [(municipio, municipio)]
            
            #--Validación de imágenes--#
            files = request.FILES.getlist('imagenes')
            if len(files) > MAX_IMAGES_PER_POST:
                data['event'] = ERROR_12
                ban_images = False
           
            for f in files:
                if f.size > MAX_IMAGE_MB * 1024 * 1024:
                    data['event'] = ERROR_13
                    ban_images = False
                    
                if not f.content_type.startswith('image/'):
                    data['event'] = ERROR_14
                    ban_images = False
                    
            if ban_images:
                if form.is_valid():
                    try:
                        inmueble_nuevo = form.save(commit=False)
                        duenio_inmueble = get_object_or_404(Usuario, pk=request.user.id)
                        inmueble_nuevo.duenio = duenio_inmueble
                        inmueble_nuevo.save()     
                        
                        for file in files:
                            imagen = Imagenes()
                            imagen.img = file
                            imagen.inmueble = inmueble_nuevo
                            imagen.save()
                               
                    except Exception as e:
                        print(e)
                else:                    
                    data['form'] = form
                    data['event'] = ERROR_2
            else:
                data['form'] = form
        else:
            data['form'] = form
            data['event'] = ERROR_3
    
    else:
        form = CrearInmuebleForm()
        departamento_id = request.GET.get('departamento_id')
        if departamento_id:
            form.fields['municipio_ubicacion'].queryset = Municipio.objects.filter(departamento_id=departamento_id)
    return render(request, HTMLCREARINMUEBLE, {**data})

@login_required
def UserEdit(request):
    """
    Vista que permite modificar los atos personales del usuario y también modificar sus datos de sesión, como su nombre de usuario o contraseña.
    Args:
        request (HttpRequest): Petición de http realizada por el usuario.
    Returns:
        HttpResponse: Renderizado gráfico de documento HTML con datos desde el servidor.
    """
    #--Variables--#
    user = request.user
    data = {}
    
    #--Procesamiento de petición--#
    if request.method == 'POST':
        #--Procesamiento de formularios--#
        if 'acc_data' in request.POST: #Cambiar datos personales
            form = EditAccountBasics(request.POST, instance=user)
            if form.is_valid():
                form.save()
                data['acc_data_event'] = SUCCESS_1
                data['acc_badge_bg'] = 'bg-success'
            else:
                data['acc_data_event'] = ERROR_2
                data['acc_badge_bg'] = 'bg-danger'
        elif 'username_data' in request.POST: #Cambiar nombre de usuario
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
                
        elif 'dz_data' in request.POST: #Cambiar datos de la zona de pelicro (contraseña)
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
        
#--------------APIS-------------#
def municipios_por_departamento(request):
    return JsonResponse(list(Municipio.objects.filter(departamento_id=request.GET.get('departamento_id')).values('id','description')), safe=False)