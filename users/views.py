from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pathlib import Path

from .forms import EditarUserProfileForm
from base.models import Perfil

from comments.models import *
# Create your views here.


def UserProfile(request, pk):
    usuario = User.objects.get(username=pk)

    perfil = Perfil.objects.get(user=usuario)
    foto_de_perfil = perfil.foto_de_perfil


    context = {
        "usuario":usuario,
        "foto_de_perfil":foto_de_perfil,
        "perfil":perfil
    }
    return render(request, "users/profile_user.html", context)


@login_required(login_url='/login')
def EditarUserProfile(request, pk):
    usuario = User.objects.get(username=pk)

    perfil = Perfil.objects.get(user=usuario)
    
    if request.method == 'POST':
        Path(perfil.foto_de_perfil.path).unlink(missing_ok=True)
        profile_form = EditarUserProfileForm(request.POST, request.FILES)
        
        if profile_form.is_valid():

            perfil.bio = profile_form.cleaned_data['bio']
            perfil.foto_de_perfil = profile_form.cleaned_data['foto_de_perfil']
            
            perfil.save()
            return redirect('user', pk)

    else:
        profile_form = EditarUserProfileForm(instance=perfil)

    context = {
        "profile_form":profile_form,
    }
    return render(request, "users/editar_profile.html", context)