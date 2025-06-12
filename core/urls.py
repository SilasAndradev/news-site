from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from news.views import (
    newsPublish, 
    newsEdit, 
    newsDelete, 
    newsPage, 
    Search,
    
    )

from users.views import (
    UserProfile,
    EditUserProfile,
    BlockProfile,
    DeleteAllUserComments,
    CommentDelete,
    )

from .views import (
    RedirectToHome,
    HomePage,
    NotFoundPage,
    LoginPage,
    LogoutUser,
    RegisterUser,
)

"""
@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
"""


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),

    # Base APP
    path('', HomePage, name='home'),
    path('404', NotFoundPage, name='404'),
    path('login/', LoginPage, name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('register/', RegisterUser, name='register'),
    
    # News APP
    path('publicar/', newsPublish, name='publicar'),
    path('editar/<str:pk>/', newsEdit, name='editar'),
    path('excluir/<str:pk>/', newsDelete, name='excluir'),
    path('noticia/<str:pk>/', newsPage, name='noticia'),
    path('noticia/feed/', newsPage, name='feed'),
    path('noticia/', RedirectToHome),
    path('search/', Search, name='search'),

    # Users APP
    path('u/', RedirectToHome),
    path('u/<str:pk>', UserProfile, name='user'),
    path('u/editar/<str:pk>', EditUserProfile, name='editar_user'),



    path('u/delete/<str:pk>', CommentDelete, name='delete-comment'),

    path('u/delete_all_comments/<str:pk>', DeleteAllUserComments, name='delete-comments'),

    path('u/block/<str:pk>', BlockProfile, name='block-user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)