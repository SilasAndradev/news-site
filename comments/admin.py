from django.contrib import admin
from .models import Comentario, Resposta, GosteiComentario, GosteiResposta
# Register your models here.

admin.site.register(Comentario)
admin.site.register(Resposta)
admin.site.register(GosteiComentario)
admin.site.register(GosteiResposta)