<<<<<<< HEAD
from .models import Resposta, Comentario
from django import forms
from django.forms import ModelForm

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Escreva seu comentário ...'})
        }
        labels = {
            'body': ''
        }
        
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model = Resposta
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Escreva sua resposta ...', 'class': "!text-sm"})
        }
        labels = {
            'body': ''
=======
from .models import Resposta, Comentario
from django import forms
from django.forms import ModelForm

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Escreva seu comentário ...'})
        }
        labels = {
            'body': ''
        }
        
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model = Resposta
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Escreva sua resposta ...', 'class': "!text-sm"})
        }
        labels = {
            'body': ''
>>>>>>> 6dad46b28fb6462401944f0f9a31339fde9957db
        }