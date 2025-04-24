from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core import exceptions
from django.db.models import Q
from pathlib import Path

from .forms import NoticiaForm, ArquivosForm, ArquivoFormSet
from base.models import Perfil
from comments.models import Comentario, Resposta
from .models import Noticia, ArquivoNaNoticia



@login_required(login_url='/login')
def NoticiaPublicar(request):
    if request.method == 'POST':
        noticia_form = NoticiaForm(request.POST, request.FILES)
        arquivo_form = ArquivosForm(request.POST, request.FILES)
            
        if noticia_form.is_valid() and arquivo_form.is_valid():
            noticia = noticia_form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            
            for arquivo in request.FILES.getlist('arquivos'):
                ArquivoNaNoticia.objects.create(noticia=noticia, arquivos=arquivo)
            
            return redirect('feed')
    else:
        noticia_form = NoticiaForm()
        arquivo_form = ArquivosForm()
        
        
    context = {
        'arquivo_form':arquivo_form,
        'noticia_form':noticia_form,
        'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
    }
    return render(request, "news/noticia_form.html", context)




def NoticiaPage(request, pk):
    if pk.isnumeric():
        noticia = get_object_or_404(Noticia, pk=pk)
        arquivos = list(ArquivoNaNoticia.objects.filter(noticia=noticia).values('arquivos'))
        comentarios = list(Comentario.objects.filter(noticia=noticia).order_by('-created'))

        if noticia.visivel or (noticia.visivel and request.user.is_staff):
            conteudo_html = noticia.corpo
            perfil = Perfil.objects.get(user=request.user) if request.user.is_authenticated else None

            if request.method == 'POST':
                if not request.user.is_authenticated:
                    return redirect('login')
                
                if not perfil.pode_comentar:
                    return HttpResponse('<h1>Você está proibido de comentar</h1>')

                body = request.POST.get('body', '').strip()
                if not body:
                    return JsonResponse({'error': 'Comentário não pode estar vazio.'}, status=400)

                comentario = Comentario.objects.create(
                    autor=perfil,
                    noticia=noticia,
                    body=body
                )

                return JsonResponse({
                    'id': comentario.id,
                    'body': comentario.body,
                    'autor': comentario.autor.user.username,
                    'foto': comentario.autor.foto_de_perfil.url if hasattr(comentario.autor.foto_de_perfil, 'url') else f"/media/{comentario.autor.foto_de_perfil}",
                    'data': comentario.created.strftime('%d %b %Y - %H:%M')
                })

            context = {
                'conteudo_html': conteudo_html,
                'noticia': noticia,
                'arquivos': arquivos,
                'comentarios': comentarios,
                'foto_de_perfil': perfil.foto_de_perfil if perfil else None
            }

            if not noticia.visivel:
                context['aviso'] = "Essa notícia não está visível para os usuários"

            return render(request, "news/noticia_page.html", context)

        else:
            return redirect('feed')

    elif pk == 'feed':
        noticias = Noticia.objects.all().order_by('-updated')
        perfil = Perfil.objects.get(user=request.user) if request.user.is_authenticated else None
        return render(request, "news/news.html", {
            'noticias': noticias,
            'foto_de_perfil': perfil.foto_de_perfil if perfil else None
        })

    return redirect('home')
    
    
@login_required(login_url='/login')
def NoticiaEditar(request, pk):

    noticia = Noticia.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("<h1>Somente o autor pode alterar alguma coisa dessa notícia!</h1>")


    if request.method == 'POST':

        noticia_form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        arquivos_formset = ArquivoFormSet(request.POST, request.FILES, queryset=ArquivoNaNoticia.objects.filter(noticia=noticia))
        arquivos = ArquivoNaNoticia.objects.filter(noticia=noticia)


        if noticia_form.is_valid() and arquivos_formset.is_valid():
            noticia = noticia_form.save(commit=False)
            noticia.autor = request.user
            arquivos = arquivos_formset.save(commit=False)
            noticia_form.save()
            
            # Esse loop vai salvar os arquivos editados
            for arquivo in arquivos:
                arquivo.noticia = noticia
                arquivo.save()
            
            
            # Esse loop vai deletar os arquivos
            for obj in arquivos_formset.deleted_objects:
                arquivos = ArquivoNaNoticia.objects.filter(noticia=obj.noticia)

                for arquivo in arquivos:
                    try:
                        Path(arquivo.arquivos.path).unlink(missing_ok=True)  # apaga do disco
                        arquivo.delete()  # apaga do banco
                    except Exception as e:
                        print(f"Erro ao excluir {arquivo.arquivos.name}: {e}")

                obj.delete()  

                
            novos_arquivos = request.FILES.getlist('novos_arquivos')
            
            # Esse loop vai criar novos Arquivos
            for arq in novos_arquivos:
                ArquivoNaNoticia.objects.create(noticia=noticia, arquivos=arq)
            
            return redirect('home')

    else:
        noticia_form = NoticiaForm(instance=noticia)
        arquivos_formset = ArquivoFormSet(queryset=ArquivoNaNoticia.objects.filter(noticia=noticia))

    foto_de_perfil = Perfil.objects.get(user=request.user).foto_de_perfil


    context = {
        'noticia_form': noticia_form,
        'arquivos_formset': arquivos_formset,
        'noticia': noticia,
        'foto_de_perfil':foto_de_perfil
    }
    return render(request, "news/editar.html", context)



@login_required(login_url='/login')
def NoticiaExcluir(request, pk):
    noticia = Noticia.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("<h1>Somente o autor pode alterar alguma coisa dessa notícia!</h1>")

    if request.method == 'POST':
        # Exclui arquivos relacionados à notícia
        arquivos = ArquivoNaNoticia.objects.filter(noticia=noticia.id)
        for arquivo in arquivos:
            try:
                Path(arquivo.arquivos.path).unlink(missing_ok=True)
            except Exception as e:
                print(f"Erro ao excluir : {e}")
        arquivos.delete()
        
        
        # Exclui possíveis arquivos diretos da notícia
        if noticia.capa_noticia:
            Path(noticia.capa_noticia.path).unlink(missing_ok=True)
        if noticia.corpo:
            Path(noticia.corpo.path).unlink(missing_ok=True)

        noticia.delete()
        return redirect('feed')

    return render(request, "news/excluir.html", {
                                                'obj': noticia,
                                                'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
                                                })
