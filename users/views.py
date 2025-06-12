from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from pathlib import Path

from .forms import EditUserProfileForm
from .models import ReaderProfile
from news.views import CommentsForm

# Create your views here.


def UserProfile(request, pk):
    user = User.objects.get(username=pk)

    context = {
        "user":user,
        "ProfilePictureUser":ReaderProfile.objects.get(user=request.user).ProfilePicture if request.user.is_authenticated else None,
        "ReaderProfile":ReaderProfile.objects.get(user=user)
    }
    return render(request, "users/profile_user.html", context)


@login_required(login_url='/login')
def EditUserProfile(request, pk):
    user = User.objects.get(username=pk)

    if request.user.username != pk and not request.user.is_staff:
        return redirect('user', pk)

    ReaderProfileUser = ReaderProfile.objects.get(user=user)
    
    ReaderProfileRequestUser = ReaderProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile_form = EditUserProfileForm(request.POST, request.FILES)
        
        if profile_form.is_valid():
            ReaderProfileUser.bio = profile_form.cleaned_data['bio']
            if profile_form.cleaned_data['ProfilePicture']:
                Path(ReaderProfileUser.ProfilePicture.path).unlink(missing_ok=True)
                ReaderProfileUser.ProfilePicture = profile_form.cleaned_data['ProfilePicture']
            
            ReaderProfileUser.save()
            return redirect('user', pk)

    else:
        profile_form = EditUserProfileForm(instance=ReaderProfileUser)
    context = {
        "profile_form":profile_form,
        "ProfilePictureUser":ReaderProfileRequestUser.ProfilePicture,
    }
    return render(request, "users/editar_profile.html", context)

@login_required(login_url='/login')
def BlockProfile(request, pk):
    if request.user.is_staff:
        profile = ReaderProfile.objects.get(id=pk)
        if profile.CommentPermission:
            profile.CommentPermission = False
            profile.save()
        else:
            profile.CommentPermission = True
            profile.save()
        return HttpResponse("<h1>Operação concluída com sucesso</h1>")
    else:
        return redirect('home')


@login_required(login_url='/login')
def DeleteAllUserComments(request, pk):
    if request.user.is_staff:
        profile = ReaderProfile.objects.get(id=pk)
        profile.CommentPermission = False
        profile.save()
        comments = list(CommentsForm.objects.filter(autor=profile))
        for comment in comments:
            comment.delete()
        return HttpResponse("<h1>All comments have been successfully deleted</h1>")
    else:
        return redirect('home')
    
@login_required(login_url='/login')
def CommentDelete(request, pk):
    if request.user.is_staff:
        comment = CommentsForm.objects.get(id=pk)
        comment.delete()
        return HttpResponse("Comment successfully deleted</h1>")
    else:
        return redirect('home')
