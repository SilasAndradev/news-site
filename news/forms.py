from .models import News,NewsArchives, NewsComments
from django.forms import modelformset_factory
from django.forms import ModelForm
from django import forms

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


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ['author', 'visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'id': 'id_corpo'}),
            'news_cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ArchivesForm(forms.ModelForm):
    arquivos = MultipleFileField()
    class Meta:
        model = NewsArchives
        fields = ['archives']
        widgets = {
            'archives': MultipleFileInput(attrs={'class': 'form-control'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['archives'].required = False

ArchivesFormSet = modelformset_factory(
    NewsArchives, 
    form=ArchivesForm, 
    extra=0, 
    can_delete=True
    )

class CommentsForm(forms.ModelForm):
    class Meta:
        model = NewsComments
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your comment...',
                'style': 'resize:none;margin-left:20px'
            })
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = NewsComments
        fields = ["body", "parent"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your answer...',
                'style': 'resize:none;margin-left:20px'
            }),
            "parent": forms.HiddenInput()
        }