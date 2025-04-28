from django.shortcuts import render
from news.models import Noticia
from base.models import Perfil
from django.db.models import Q
# Create your views here.

def Procurar(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    número_de_notícia = 0
    noticias = Noticia.objects.all().order_by('-updated').filter(
        Q(título__icontains=q) &
        Q(visivel=True)
        )
    número_de_notícia = noticias.count()
    if request.user.is_authenticated:  
        foto_de_perfil = Perfil.objects.get(user=request.user).foto_de_perfil
    else:
        foto_de_perfil = None
    context = {
        'noticias':noticias,    
        'número_de_notícia':número_de_notícia,
        'foto_de_perfil':foto_de_perfil
    }
    return render(request, "busca/procurar.html", context)