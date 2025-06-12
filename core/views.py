from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

from news.models import News
from users.models import ReaderProfile


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
        except Exception:
            messages.error(request, "Users don't exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username OR password!')

    context = {

    }
    return render(request, 'core/login.html', context)


def RegisterUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            reader = ReaderProfile.objects.create(
                user = user,
                CommentPermission = True, 
                PermissionChangeProfile = True,
                ProfilePicture = "uploads/perfis/default.jpg",
                bio = "Eu sou novo aqui!"
            )
            reader.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')
    return render(request, 'core/register.html', {'form':form})

@login_required(login_url='/login')
def LogoutUser(request):
    logout(request)
    return redirect('home')


def HomePage(request):

    news = News.objects.all().order_by('-updated_at')[:10]  
    if request.user.is_authenticated:
        perfil = ReaderProfile.objects.filter(user=request.user)
        context = {
        'news':news,
        'perfil':perfil,
        'ProfilePictureUser':ReaderProfile.objects.get(user=request.user).ProfilePicture
    }
    else:
        context = {
            'news':news,
            'perfil':None,
            'ProfilePictureUser':None
        }
    return render(request, "core/index.html", context)


