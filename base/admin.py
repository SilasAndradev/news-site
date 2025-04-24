from django.contrib import admin

# Register your models here.
from .models import Perfil
from news.models import *
from comments.models import *
from users.models import *

admin.site.register(Perfil)
admin.site.register(Noticia)
admin.site.register(ArquivoNaNoticia)
