from django.forms import ModelForm
from users.models import ReaderProfile
from django import forms

class EditUserProfileForm(ModelForm):
    class Meta:
        model = ReaderProfile
        fields = ['bio', 'ProfilePicture']
        exclude = ['user']
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
            'ProfilePicture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ProfilePicture'].required = False