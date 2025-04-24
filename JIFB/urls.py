"""
URL configuration for lancode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from news.views import NoticiaPublicar, NoticiaEditar, NoticiaExcluir, NoticiaPage
from busca.views import Procurar
from users.views import *
from base.views import *
from comments.views import *
"""
@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
"""


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include('base.urls')),
    
    path('publicar/', NoticiaPublicar, name='publicar'),
    path('editar/<str:pk>/', NoticiaEditar, name='editar'),
    path('excluir/<str:pk>/', NoticiaExcluir, name='excluir'),
    path('noticia/<str:pk>/', NoticiaPage, name='noticia'),
    path('noticia/feed/', NoticiaPage, name='feed'),

    path('procurar/', Procurar, name='procurar'),

    path('u/', RedirectToHome),
    path('u/<str:pk>', UserProfile, name='user'),
    path('u/editar/<str:pk>', EditarUserProfile, name='editar_user'),

    path('excluir-comentario/<str:pk>/', ComentarioExcluir, name='excluir-comentario'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)