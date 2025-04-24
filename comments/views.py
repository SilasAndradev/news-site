from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from .models import Comentario
from base.models import Perfil
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login')
def ComentarioExcluir(request, pk):
    comentario = Comentario.objects.get(id=pk)
    if request.method == 'POST':
        # Exclui arquivos relacionados à notícia
        if request.user.is_staff == False or request.user.username != comentario.autor.user.username:
            return HttpResponse("<h1>Somente o autor ou um moderador pode excluir!</h1>")
        
        elif request.user.is_staff == True or request.user.username == comentario.autor.user.username:
            comentario.delete()
        
        return redirect('noticia', comentario.noticia.id)

    return render(request, "comments/excluir.html", {
                                                'obj': comentario,
                                                'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
                                                })