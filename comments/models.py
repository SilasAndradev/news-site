from django.db import models
from base.models import *
from news.models import Noticia

class Comentario(models.Model):
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comments', default=None)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    like = models.IntegerField(blank=True, null=True, default=0)
    dislike = models.IntegerField(blank=True, null=True, default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.autor.user.username} : {self.body[0:30]}'

class GosteiComentario(models.Model):
    comment = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.perfil.user.username} : {self.comment.body[:30]}'

class Resposta(models.Model):
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='replies')
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    like = models.IntegerField(blank=True, null=True, default=0)
    dislike = models.IntegerField(blank=True, null=True, default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.autor.user.username} : {self.body[0:30]}'
    
class GosteiResposta(models.Model):
    resposta = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.perfil.user.username} : {self.comment.body[:30]}'