from django.forms import ModelForm
from .models import Noticia, ArquivoNaNoticia
from django import forms
from django.forms import modelformset_factory

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class NoticiaForm(ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'
        exclude = ['autor']
        widgets = {
            'título': forms.TextInput(attrs={'class': 'form-control'}),
            'corpo': forms.FileInput(attrs={'class': 'form-control'}),
            'capa_noticia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'visivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ArquivosForm(forms.ModelForm):
    arquivos = MultipleFileField()
    class Meta:
        model = ArquivoNaNoticia
        fields = ['arquivos']
        widgets = {
            'arquivos': MultipleFileInput(attrs={'class': 'form-control'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['arquivos'].required = False

ArquivoFormSet = modelformset_factory(
    ArquivoNaNoticia, 
    form=ArquivosForm, 
    extra=0, 
    can_delete=True
    )