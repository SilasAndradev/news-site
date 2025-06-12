from django.contrib.auth.models import User
from users.models import ReaderProfile
from django.db import models

# Create your models here.

class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    
    body = models.FileField(upload_to="uploads/noticias/tempFile/")
    news_cover = models.ImageField(upload_to="uploads/noticias/CAPAS/%Y/%m/%d")

    visible = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class NewsArchives(models.Model):
    news = models.ForeignKey(News, related_name='arquivos', on_delete=models.CASCADE)
    archives = models.FileField(upload_to="uploads/noticias/arquives/", blank=True, null=True)

    def __str__(self):
        return f"Archive from {self.news.title}"


class NewsComments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comentarios")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="respostas")
    author = models.ForeignKey(ReaderProfile, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:13] + "..." + "por" + " " + self.author.user.username 

    