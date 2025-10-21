# news/urls.py

from django.urls import path
from . import views 

from news.views import (
    newsPublish, 
    newsEdit, 
    newsDelete, 

    upload_tinymce_image,
    #FeedNoticiasView,
    MeusArtigos
    )

urlpatterns = [
    path('post-news/', newsPublish, name='post-news'),
    path('edit/<str:pk>/', newsEdit, name='edit-news'),
    path('delete/<str:pk>/', newsDelete, name='delete-news'),


    path('upload_image_tinymce/', upload_tinymce_image, name='upload_tinymce_image'),
    
    
    
    path('meus-artigos/', MeusArtigos, name='meus_artigos'), 
]