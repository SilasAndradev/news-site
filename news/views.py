from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from pathlib import Path
import markdown
import os

from .forms import (
    NewsForm, 
    ArchivesForm, 
    ArchivesFormSet, 
    CommentsForm, 
    ResponseForm
    )
from .models import (
    News, 
    NewsArchives, 
    NewsComments
    )
from users.models import ReaderProfile




@login_required(login_url='/login')
def newsPublish(request):
    if request.method == 'POST':
        news_form = NewsForm(request.POST, request.FILES)
        arquivo_form = ArchivesForm(request.POST, request.FILES)
            
        if news_form.is_valid() and arquivo_form.is_valid():
            news = news_form.save(commit=False)
            news.author = request.user

             # Lê o conteúdo Markdown do arquivo enviado
            # Primeiro, salve a notícia com o arquivo markdown
            news.save()

            # Agora leia o conteúdo do arquivo markdown enviado
            if news.body:
                markdown_file = news.body

                # Abrir o arquivo salvo no servidor
                with markdown_file.open(mode='rb') as f:
                    markdown_content = f.read().decode('utf-8')

                # Converte para HTML
                html_content = markdown.markdown(markdown_content)

                # Gera caminho do arquivo HTML com base na data/hora
                now = timezone.now()
                file_name = now.strftime(f"{news.title}") + ".html"
                html_path = os.path.join("uploads", "news", now.strftime(f"%Y/%m/%d/{news.title}"))
                full_path = os.path.join(settings.MEDIA_ROOT, html_path)
                os.makedirs(full_path, exist_ok=True)

                full_file_path = os.path.join(full_path, file_name)
                relative_file_path = os.path.join(html_path, file_name)

                # Salva o conteúdo HTML em um novo arquivo
                with open(full_file_path, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)

                # Atualiza o campo corpo com o caminho do HTML gerado
                news.body.name = relative_file_path
                Path(markdown_file).unlink(missing_ok=True)
                news.save()

            # Salva archives adicionais, se existirem
            for arquivo in request.FILES.getlist('archives'):
                if arquivo:
                    NewsArchives.objects.create(news=news, archives=arquivo)

            return redirect('feed')
            
    else:
        news_form = NewsForm()
        arquivo_form = ArchivesForm()
        
        
    context = {
        'arquivo_form':arquivo_form,
        'news_form':news_form,
        'ProfilePictureUser':ReaderProfile.objects.get(user=request.user).ProfilePicture
    }
    return render(request, "news/news_form.html", context)




def newsPage(request, pk):
    if pk.isnumeric():
        news = get_object_or_404(News, id=pk)
        archives = NewsArchives.objects.filter(news=news)
        comentarios = NewsComments.objects.filter(news=news).order_by('-data')

        if news.visivel or ( not news.visivel and request.user.is_staff):
            conteudo_html = news.corpo
            perfil = ReaderProfile.objects.get(user=request.user) if request.user.is_authenticated else None

            if request.method == 'POST' and request.user.is_authenticated:
                if not perfil.pode_comentar:
                    return HttpResponse('<h1>Você está proibido de comentar</h1>')

                if 'pai' in request.POST and request.POST.get('pai'):  # É resposta
                    form = ResponseForm(request.POST)
                else:
                    form = CommentsForm(request.POST)

                if form.is_valid():
                    comentario = form.save(commit=False)
                    comentario.autor = perfil
                    comentario.news = news
                    comentario.save()
                    return redirect('news', pk=pk)

            context = {
                'conteudo_html':conteudo_html,
                'news': news,
                'archives': archives,
                'comentarios': comentarios,
                'comentario_form': CommentsForm(),
                'resposta_form': ResponseForm(),
                'ProfilePictureUser': perfil.ProfilePicture if perfil else None,
                'perfil': perfil,
                'numero_de_comentarios': len(comentarios)
            }

            if not news.visivel:
                context['aviso'] = "Essa notícia não está visível para os usuários"

            return render(request, "news/news_page.html", context)
        else:
            return redirect('feed')

    elif pk == 'feed':
        newss = News.objects.all().order_by('-updated')
        perfil = ReaderProfile.objects.get(user=request.user) if request.user.is_authenticated else None
        return render(request, "news/feed.html", {
            'newss': newss,
            'ProfilePictureUser': perfil.ProfilePicture if perfil else None
        })
    else:
        return redirect('feed')
    
    
@login_required(login_url='/login')
def newsEdit(request, pk):

    news = News.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("<h1>Somente o autor pode alterar alguma coisa dessa notícia!</h1>")


    if request.method == 'POST':

        news_form = NewsForm(request.POST, request.FILES, instance=news)
        archives_formset = ArchivesFormSet(request.POST, request.FILES, queryset=NewsArchives.objects.filter(news=news))
        archives = NewsArchives.objects.filter(news=news)


        if news_form.is_valid() and archives_formset.is_valid():
            news = news_form.save(commit=False)
            news.autor = request.user
            archives = archives_formset.save(commit=False)
            news_form.save()
            
            if news.corpo:
                markdown_file = news.corpo

                # Abrir o arquivo salvo no servidor
                with markdown_file.open(mode='rb') as f:
                    markdown_content = f.read().decode('utf-8')

                # Converte para HTML
                html_content = markdown.markdown(markdown_content)

                now = timezone.now()
                file_name = now.strftime(f"{news.title}") + ".html"
                html_path = os.path.join("uploads", "news", now.strftime(f"%Y/%m/%d/{news.title}"))
                full_path = os.path.join(settings.MEDIA_ROOT, html_path)
                os.makedirs(full_path, exist_ok=True)

                full_file_path = os.path.join(full_path, file_name)
                relative_file_path = os.path.join(html_path, file_name)

                # Salva o conteúdo HTML em um novo arquivo
                with open(full_file_path, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)

                # Atualiza o campo corpo com o caminho do HTML gerado
                news.body.name = relative_file_path
                news.save()

            # Esse loop vai salvar os archives editados
            for archive in archives:
                archive.news = news
                archive.save()
            
            
            # Esse loop vai deletar os archives
            for obj in archives_formset.deleted_objects:
                archives = NewsArchives.objects.filter(news=obj.news)

                for archive in archives:
                    try:
                        Path(archive.archives.path).unlink(missing_ok=True)  # apaga do disco
                        archive.delete()  # apaga do banco
                    except Exception as e:
                        print(f"Erro ao excluir {archive.archives.name}: {e}")

                obj.delete()  

                
            new_files = request.FILES.getlist('new_files')
            
            # Esse loop vai criar novos Arquivos
            for file in new_files:
                NewsArchives.objects.create(news=news, archives=file)
            
            return redirect('home')

    else:
        news_form = NewsForm(instance=news)
        archives_formset = ArchivesFormSet(queryset=NewsArchives.objects.filter(news=news))

    ProfilePicture = ReaderProfile.objects.get(user=request.user).ProfilePicture


    context = {
        'news_form': news_form,
        'archives_formset': archives_formset,
        'news': news,
        'ProfilePictureUser':ProfilePicture
    }
    return render(request, "news/editar.html", context)



@login_required(login_url='/login')
def newsDelete(request, pk):
    news = News.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("<h1>Somente o autor pode alterar alguma coisa dessa notícia!</h1>")

    if request.method == 'POST':
        # Exclui archives relacionados à notícia
        archives = NewsArchives.objects.filter(news=news.id)
        for arquivo in archives:
            try:
                Path(arquivo.archives.path).unlink(missing_ok=True)
            except Exception:
                pass
        archives.delete()
        
        
        if news.capa_news:
            Path(news.capa_news.path).unlink(missing_ok=True)
        if news.corpo:
            Path(news.corpo.path).unlink(missing_ok=True)

        news.delete()
        return redirect('feed')

    return render(request, "news/excluir.html", {
                                                'obj': news,
                                                'ProfilePictureUser':ReaderProfile.objects.get(user=request.user).ProfilePicture
                                                })


def Search(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    news = News.objects.all().order_by('-updated_at').filter(
        Q(title__icontains=q) &
        Q(visible=True)
        )
    if request.user.is_authenticated:  
        ProfilePicture = ReaderProfile.objects.get(user=request.user).ProfilePicture
    else:
        ProfilePicture = None
    context = {
        'news':news,    
        'NumberNews':news.count(),
        'ProfilePictureUser':ProfilePicture
    }
    return render(request, "news/procurar.html", context)