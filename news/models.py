from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Noticia(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    título = models.CharField(max_length=500)
    
    corpo = models.FileField(upload_to="uploads/noticias/%Y/%m/%d/")
    capa_noticia = models.ImageField(upload_to="uploads/noticias/CAPAS/%Y/%m/%d/")

    visivel = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.título


class ArquivoNaNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, related_name='arquivos', on_delete=models.CASCADE)
    arquivos = models.FileField(upload_to="uploads/noticias/arquivos/", blank=True, null=True)

    def __str__(self):
        return f"Arquivo de {self.noticia.título}"
