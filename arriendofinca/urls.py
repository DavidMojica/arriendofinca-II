"""
URL configuration for arriendofinca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('userarea/',views.UserArea, name='userarea'),
    path('useredit/', views.UserEdit, name='useredit'),
    path('crear_inmueble/', views.CrearInmueble, name="crear_inmueble"),
    path('editar_inmueble/<int:inmueble_id>/', views.EditarInmueble, name="editar_inmueble"),
    path('busqueda/',views.Busqueda, name="busqueda"),
    path('detalles_inmueble/<int:inmueble_id>/', views.DetallesInmueble, name='detalles_inmueble'),
    path('FAQS/', views.Faqs, name='FAQS'),
    #APIS#
    path('municipios_por_departamento/', views.municipios_por_departamento, name='municipios_por_departamento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
