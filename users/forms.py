from django.forms import ModelForm
from base.models import Perfil
from django import forms

class EditarUserProfileForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['bio', 'foto_de_perfil']
        exclude = ['user']
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_de_perfil': forms.FileInput(attrs={'class': 'form-control'}),
        }
