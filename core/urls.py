from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include



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
    QuemSomosPage
    
)
from news.views import newsPage

"""
@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
"""


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),

    # Core APP
    path('', HomePage, name='home'),
    path('404', NotFoundPage, name='404'),
    path('login/', LoginPage, name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('register/', RegisterUser, name='register'),
    path('quem-somos/', QuemSomosPage, name='quem_somos'),
    # News APP
    path('news/', include('news.urls')), 
    path('news/<str:pk>/', newsPage, name='news'),
    # Users APP
    path('u/', RedirectToHome),
    path('u/<str:pk>', UserProfile, name='user'),
    path('u/edit/<str:pk>', EditUserProfile, name='edit-user'),



    path('u/delete/<str:pk>', CommentDelete, name='delete-comment'),

    path('u/delete_all_comments/<str:pk>', DeleteAllUserComments, name='delete-comments'),

    path('u/block/<str:pk>', BlockProfile, name='block-user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
                          )