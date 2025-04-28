from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from pathlib import Path

from .models import Perfil
from news.models import Noticia

def QuemSomosPage(request):
    return render(request, 'base/quemsomos.html', {'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil if request.user.is_authenticated else None})


def RedirectToHome(request):
    return redirect('home')


def NotFoundPage(request):
    return render(request, '404.html')


def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Usuário não existe!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nome de usuário OU senha estão erradas!')

    context = {

    }
    return render(request, 'base/login.html', context)


def RegisterUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            Perfil.objects.create(
                user=user,
                pode_comentar=True,
                pode_alterar_foto_de_perfil=True,
                foto_de_perfil="foto_de_perfis/default.jpg"
            )

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ocorreu um erro durante o registro!')
    return render(request, 'base/register.html', {'form':form})

@login_required(login_url='/login')
def LogoutUser(request):
    logout(request)
    return redirect('home')


def HomePage(request):

    noticias = Noticia.objects.all().order_by('-updated')
    if request.user.is_authenticated:
        perfil = Perfil.objects.filter(user=request.user)
        context = {
        'noticias':noticias,
        'perfil':perfil,
        'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
    }
    else:
        context = {
            'noticias':noticias,
            'perfil':None,
            'foto_de_perfil':None
        }
    return render(request, "base/index.html", context)


