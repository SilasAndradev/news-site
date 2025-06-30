from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from pathlib import Path
import os

from django.http import JsonResponse 
from django.core.files.storage import default_storage 
from django.views.decorators.csrf import csrf_exempt 
import bleach

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

            news.save()

            if news.body:
                allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [ 
                    'img', 'video', 'source', 'iframe', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'blockquote', 'pre', 'code', 'table',
                    'thead', 'tbody', 'tr', 'th', 'td'
                ]
                allowed_attrs = {
                    **bleach.sanitizer.ALLOWED_ATTRIBUTES, 
                    'img': ['src', 'alt', 'width', 'height', 'style'],
                    'a': ['href', 'title', 'target', 'rel'],
                    'iframe': ['src', 'width', 'height', 'allowfullscreen', 'frameborder'],
                    'video': ['src', 'controls', 'width', 'height'],
                    'source': ['src', 'type'],
                    '*': ['style', 'class', 'id'], 
                }
                

                news.body = bleach.clean(
                    news.body,
                    tags=allowed_tags,
                    attributes=allowed_attrs,
                    strip=True
                )

                news.save()

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



@csrf_exempt 
@login_required(login_url='/login')
def upload_tinymce_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        img_file = request.FILES['file']
        
        upload_dir = os.path.join('uploads', 'news', 'editor_images', timezone.now().strftime("%Y/%m/%d/"))
        
     
        full_upload_path = os.path.join(settings.MEDIA_ROOT, upload_dir)
        os.makedirs(full_upload_path, exist_ok=True)

        file_path_in_media = default_storage.save(os.path.join(upload_dir, img_file.name), img_file)

      
        file_url = request.build_absolute_uri(default_storage.url(file_path_in_media))
        
        return JsonResponse({'location': file_url}) # TinyMCE espera uma resposta JSON com o campo 'location'
    return JsonResponse({'error': 'No image file uploaded'}, status=400)

def newsPage(request, pk):
    news = News.objects.get(id=pk)
    archives = NewsArchives.objects.filter(news=news)
    comentarios = NewsComments.objects.filter(news=news).order_by('-data')

    if news.visivel or ( not news.visivel and request.user.is_staff):
        conteudo_html = news.corpo
        perfil = ReaderProfile.objects.get(user=request.user) if request.user.is_authenticated else None

        if request.method == 'POST' and request.user.is_authenticated:
            if perfil.CommentPermission:
                if 'pai' in request.POST and request.POST.get('pai'):  # É resposta
                    form = ResponseForm(request.POST)
                else:
                    form = CommentsForm(request.POST)

                if form.is_valid():
                    comentario = form.save(commit=False)
                    comentario.author = perfil
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

        if not news.visible:
            context['aviso'] = "Essa notícia não está visível para os usuários"

        return render(request, "news/news_page.html", context)
    else:
        return redirect('home')

    
    
@login_required(login_url='/login')
def newsEdit(request, pk):

    news = News.objects.get(id=pk)

    if not request.user.is_staff:
        return redirect('noticia', pk=pk)


    if request.method == 'POST':

        news_form = NewsForm(request.POST, request.FILES, instance=news)
        archives_formset = ArchivesFormSet(request.POST, request.FILES, queryset=NewsArchives.objects.filter(news=news))
        archives = NewsArchives.objects.filter(news=news)


        if news_form.is_valid() and archives_formset.is_valid():
            news = news_form.save(commit=False)
            news.author = request.user
            archives = archives_formset.save(commit=False)
            news_form.save()
            
            if news.body:
                allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [ 
                    'img', 'video', 'source', 'iframe', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'blockquote', 'pre', 'code', 'table',
                    'thead', 'tbody', 'tr', 'th', 'td'
                ]
                allowed_attrs = {
                    **bleach.sanitizer.ALLOWED_ATTRIBUTES, 
                    'img': ['src', 'alt', 'width', 'height', 'style'],
                    'a': ['href', 'title', 'target', 'rel'],
                    'iframe': ['src', 'width', 'height', 'allowfullscreen', 'frameborder'],
                    'video': ['src', 'controls', 'width', 'height'],
                    'source': ['src', 'type'],
                    '*': ['style', 'class', 'id'], 
                }
    
                news.body = bleach.clean(
                    news.body,
                    tags=allowed_tags,
                    attributes=allowed_attrs,
                    strip=True
                )
                news.save()

            for archive in archives:
                archive.news = news
                archive.save()
            
            
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
    return render(request, "news/update.html", context)



@login_required(login_url='/login')
def newsDelete(request, pk):
    news = News.objects.get(id=pk)

    if not request.user.is_staff:
        return redirect('noticia', pk=pk)

    if request.method == 'POST':
        archives = NewsArchives.objects.filter(news=news.id)
        for arquivo in archives:
            try:
                Path(arquivo.archives.path).unlink(missing_ok=True)
            except Exception:
                pass
        archives.delete()
        
        
        if news.news_cover:
            Path(news.news_cover.path).unlink(missing_ok=True)
        if news.body:
            Path(news.body.path).unlink(missing_ok=True)

        news.delete()
        return redirect('feed')

    return render(request, "news/delete.html", {
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
    return render(request, "news/search.html", context)


@login_required(login_url='/login') 
def MeusArtigos(request):
    meus_artigos = News.objects.filter(author=request.user).order_by('-created_at')
    perfil = ReaderProfile.objects.get(user=request.user) if request.user.is_authenticated else None

    context = {
        'meus_artigos': meus_artigos,
        'minha_foto_de_perfil': perfil.ProfilePicture if perfil else None,
        'perfil': perfil,
    }
    return render(request, 'news/meus_artigos.html', context)