import random
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import Inmueble, Municipio, TipoCobro, TipoUsuario, Usuario, Imagenes, Destacados
from .forms import FiltrarInmueblesCaracteristicas, EditarInmuebleForm, FiltrarInmuebles,CrearInmuebleForm, BusquedaInmuebleForm, LoginForm, RegisterForm, EditAccountBasics, EditAccountDangerZone
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
HTMLEDITARINMUEBLE = 'inmueble_editar.html'
HTMLBUSQUEDA = "busqueda.html"
HTMLDETALLESINMUEBLE = 'detallesinmueble.html'
HTMLFAQS = 'FAQS.html'

#--MENSAJES--#
SUCCESS_1 = "Guardado con éxito"
SUCCESS_2 = "Inmueble borrado con éxito"
SUCCESS_3 = "Imagenes guardadas correctamente"
SUCCESS_4 = "Imagen borrada correctamente"

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
ERROR_12 = f"Se excedió la cantida de imágenes. Maximo {MAX_IMAGES_PER_POST} imágenes por inmueble."
ERROR_13 = f"Alguna imagen excede el peso permitido. Máximo {MAX_IMAGE_MB} Mb por imágen"
ERROR_14 = "Algún archivo cargado NO es una imagen."
ERROR_15 = "Este objeto no existe"
ERROR_16 = "No se pudo borrar el inmueble, no se pudo garantizar autenticidad."
ERROR_17 = "Petición desconocida"

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

def ValidarImagenes(files, cantidad_imagenes_inmueble=0):
    """
    Se encarga de validar las imágenes provenientes de los formularios.

    Args:
        files (FILE_LIST): Lista de imágenes provenientes de los formularios.

    Returns:
        bool: Bandera aprobatoria de las validaciones.
        int: Número usado para mostrar errores en la salida.
    """
    if len(files) > MAX_IMAGES_PER_POST:
        return False, 0

    for f in files:
        if f.size > MAX_IMAGE_MB * 1024 * 1024:
            return False, 1
        
        if not f.content_type.startswith('image/'):
            return False, 2
    
    if cantidad_imagenes_inmueble + len(files) > MAX_IMAGES_PER_POST:
        return False, 0
      
    return True, 3
#-----------------------------------------------------------------------------------------#
#-----------------------------------------VISTAS------------------------------------------#
#-----------------------------------------------------------------------------------------#
#--HOME o Index--#
def home(request):
    data = { 'form': BusquedaInmuebleForm(),
            'inmuebles': Inmueble.objects.all().order_by('-fecha_creacion')[:4]}
    
    inmuebles_destacados = Destacados.objects.all()
    inmuebles_destacados = [destacado.inmueble for destacado in inmuebles_destacados]
    inmuebles_destacados = random.sample(list(inmuebles_destacados), min(len(inmuebles_destacados), 4))
    
    data['inmuebles_destacados'] = inmuebles_destacados
    return render(request, HTMLHOME, {**data})

def Faqs(request):
    
    return render(request, HTMLFAQS)

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
#-Borrar inmueble
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
    INMUEBLES_POR_PAGINA = 9
    data = {'form': FiltrarInmuebles(), 'event': '', 'alert_type': 'danger'}
    inmuebles_usuario = Inmueble.objects.filter(duenio=request.user.id)
    
    
    if request.method == 'POST':
        if 'eliminarPropiedad' in request.POST:
            propiedad_id = request.POST.get('propiedad_id')
            try:
                inmueble = get_object_or_404(Inmueble, pk=propiedad_id)
                if inmueble.duenio.id == request.user.id:
                    inmueble.delete()
                    data['event'] = SUCCESS_2
                    data['alert_type'] = 'success'
                else:
                    data['event'] = ERROR_16
            except Inmueble.DoesNotExist:
                data['event'] = ERROR_15
    else:
        form = FiltrarInmuebles(request.GET) #Si el formulario fue enviado por metodo get.
        if 'municipio' in request.GET:
            municipio_id = request.GET.get('municipio')
            if municipio_id:
                municipio_nombre = Municipio.objects.get(pk=municipio_id).description
                form.fields['municipio'].choices = [(municipio_id, municipio_nombre)]
        #--Procesamiento de formularios--#
        if form.is_valid():
            data['form'] = form
            #--Form de filtro--#
            id_inmueble = form.cleaned_data.get('id')
            tipo_inmueble = form.cleaned_data.get('tipo_inmueble')
            departamento = form.cleaned_data.get('departamento')
            municipio = form.cleaned_data.get('municipio')

            if id_inmueble:
                inmuebles_usuario = inmuebles_usuario.filter(id=id_inmueble)
            
            if tipo_inmueble:
                inmuebles_usuario = inmuebles_usuario.filter(tipo_inmueble=tipo_inmueble)
        
            if departamento and municipio:
                inmuebles_usuario = inmuebles_usuario.filter(municipio_ubicacion_id=municipio)
            
        else:
            data['event'] = ERROR_2
            
    paginator = Paginator(inmuebles_usuario, INMUEBLES_POR_PAGINA)
    page_number = request.GET.get('page')
    
    try:
        inmuebles_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        inmuebles_paginados = paginator.page(1)
    except EmptyPage:
        inmuebles_paginados = paginator.page(paginator.num_pages)
        
    data['inmuebles'] = inmuebles_paginados
    

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
            ERROR_LIST = [ERROR_12, ERROR_13, ERROR_14]
            ban_images, error_index = ValidarImagenes(files)
            
            if ban_images:
                if form.is_valid():
                    try:
                        inmueble_nuevo = form.save(commit=False)
                        arriendo_venta = request.POST.get('arriendo_venta')
                        
                        print(f"{arriendo_venta} - {type(arriendo_venta)}")
                        
                        if arriendo_venta == '1':
                            inmueble_nuevo.tipo_cobro = get_object_or_404(TipoCobro, pk= 5)
                            
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
                    print("Errores en el formulario:")
                    for field, errors in form.errors.items():
                        for error in errors:
                            print(f"- {field}: {error}")                    
                    data['form'] = form
                    data['event'] = ERROR_2
            else:
                data['event'] = ERROR_LIST[error_index]
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
def EditarInmueble(request,  inmueble_id):
    #Si no se proporciono id de inmueble
    if inmueble_id is None:
        return redirect('userarea')
    #Si el usuario no es el dueño de la propiedad
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id)
    if inmueble.duenio.id != request.user.id:
        return redirect('userarea')
    
    #--Si todo salió bien--#
    data = {'event' : '', 'alert_type': 'danger'}
    if request.method == 'POST':
        if 'guardar_edicion' in request.POST:
            form = EditarInmuebleForm(request.POST, instance=inmueble)
            if form.is_valid():
                inmueble_editar = form.save(commit=False)
                inmueble_editar.save()
                data['alert_type'] = 'success'
                data['event'] = SUCCESS_1
            else:
                data['event'] = ERROR_2        
        elif 'eliminarImagen' in request.POST:
            imagen_id = request.POST.get('imagen_id')   
            imagen = Imagenes.objects.get(pk=imagen_id)

            if imagen.img:     
                imagen.img.delete()
            imagen.delete()
            data['alert_type'] = 'success'
            data['event'] = SUCCESS_4
            
        elif 'agregar_imagenes' in request.POST:
            #--Validación de imágenes--#
            files = request.FILES.getlist('imagenes')
            ERROR_LIST = [ERROR_12, ERROR_13, ERROR_14]
            ban_images, error_index = ValidarImagenes(files, inmueble.imagenes.count())
            
            if ban_images:
                for file in files:
                    imagen = Imagenes()
                    imagen.img = file
                    imagen.inmueble = inmueble
                    imagen.save()
                data['alert_type'] = 'success'
                data['event'] = SUCCESS_3
            else:
                data['event'] = ERROR_LIST[error_index]
        else:
            data['event'] = ERROR_17
    
    form = EditarInmuebleForm(instance=inmueble)
    form.fields['tipo_inmueble'].choices = [(inmueble.tipo_inmueble.id, inmueble.tipo_inmueble.description)]
    form.fields['municipio_ubicacion'].choices = [(inmueble.municipio_ubicacion.id, inmueble.municipio_ubicacion.description)]
    form.fields['departamento'].choices = [(inmueble.municipio_ubicacion.departamento.id, inmueble.municipio_ubicacion.departamento.description)]
    data['form'] = form
    data['inmueble'] = inmueble
    
    return render(request, HTMLEDITARINMUEBLE, {**data} )

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
    
#----------BÚSQUEDA------------#
def Busqueda(request):
    tipo_inmueble = request.GET.get('tipo_inmueble')
    arriendo_venta = request.GET.get('arriendo_venta')
    municipio_ubicacion = request.GET.get('municipio_ubicacion')
    solo_certificados = request.GET.get('solo_certificados')
    
    inmuebles = []
    INMUEBLES_POR_PAGINA = 9
    data = { 'form_filtro': FiltrarInmueblesCaracteristicas()}
    form = BusquedaInmuebleForm(request.GET)
    #Campos obligatorios
    if tipo_inmueble:
        inmuebles = Inmueble.objects.filter(tipo_inmueble=tipo_inmueble)
    else:
        return redirect('home')
    
    if arriendo_venta:
        inmuebles = inmuebles.filter(arriendo_venta=arriendo_venta)
        
    if municipio_ubicacion:
        municipio_nombre = Municipio.objects.get(pk=municipio_ubicacion).description
        form.fields['municipio_ubicacion'].choices = [(municipio_ubicacion, municipio_nombre)]
        inmuebles = inmuebles.filter(municipio_ubicacion=municipio_ubicacion)
    
    if solo_certificados == 'on':
        inmuebles = inmuebles.exclude(certificado__isnull=True)
        
    if request.method == "POST":
        if 'filter_secondary' in request.POST:
            form_post = FiltrarInmueblesCaracteristicas(request.POST)
            if form_post.is_valid():
                precio_min = form_post.cleaned_data['precio_min']
                precio_max = form_post.cleaned_data['precio_max']
                habitaciones = form_post.cleaned_data['habitaciones']
                banios = form_post.cleaned_data['banios']
                area_min = form_post.cleaned_data['area_min']
                area_max = form_post.cleaned_data['area_max']
                
                if precio_min:
                    inmuebles = inmuebles.exclude(precio__lt=precio_min)
                
                if precio_max:
                    inmuebles =inmuebles.exclude(precio__gt=precio_max)
                    
                if habitaciones:
                    inmuebles = inmuebles.filter(habitaciones=habitaciones)
                    
                if banios:
                    inmuebles = inmuebles.filter(banios=banios)
                    
                if area_min:
                    inmuebles = inmuebles.exclude(area__lt=area_min)
                
                if area_max:
                    inmuebles= inmuebles.exclude(area__gt=area_max)
                
                data['form_filtro'] = form
            else:
                data['event'] = ERROR_2
        else:
            data['event'] = ERROR_17
        
    
    paginator = Paginator(inmuebles, INMUEBLES_POR_PAGINA)
    page_number = request.GET.get('page', 1)
    
    try:
        inmuebles_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        inmuebles_paginados = paginator.page(1)
    except EmptyPage:
        inmuebles_paginados = paginator.page(paginator.num_pages)
     
    data['form'] = form
    data['inmuebles'] = inmuebles_paginados
    return render(request, HTMLBUSQUEDA, {**data})
    
def DetallesInmueble(request,inmueble_id):
    #Si no hay ID del inmueble
    if inmueble_id is None:
        return redirect('home')
    
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id)
    data = {'inmueble':inmueble}
    
    return render(request, HTMLDETALLESINMUEBLE, {**data})
    

#--------------APIS-------------#
def municipios_por_departamento(request):
    return JsonResponse(list(Municipio.objects.filter(departamento_id=request.GET.get('departamento_id')).values('id','description')), safe=False)