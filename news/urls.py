# news/urls.py

from django.urls import path
from . import views 

from news.views import (
    newsPublish, 
    newsEdit, 
    newsDelete, 
    newsPage, 
    Search,
    upload_tinymce_image,
    #FeedNoticiasView,
    MeusArtigos
    )

urlpatterns = [
    path('post-news/', newsPublish, name='post-news'),
    path('edit/<str:pk>/', newsEdit, name='edit-user'),
    path('delete/<str:pk>/', newsDelete, name='delete-noticia'),
    path('<str:pk>/', newsPage, name='noticia'),
    path('search/', Search, name='search'),

    path('upload_image_tinymce/', upload_tinymce_image, name='upload_tinymce_image'),
    
    
    
    path('meus-artigos/', MeusArtigos, name='meus_artigos'), 
]