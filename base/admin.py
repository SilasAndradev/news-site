<<<<<<< HEAD
from django.contrib import admin

# Register your models here.
from .models import Perfil
from news.models import *
from comments.models import *
from users.models import *

admin.site.register(Perfil)
admin.site.register(Noticia)
admin.site.register(ArquivoNaNoticia)
=======
from django.contrib import admin

# Register your models here.
from .models import Perfil
from news.models import *
from comments.models import *
from users.models import *

admin.site.register(Perfil)
admin.site.register(Noticia)
admin.site.register(ArquivoNaNoticia)
>>>>>>> 6dad46b28fb6462401944f0f9a31339fde9957db
