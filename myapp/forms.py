from django import forms
from .models import Podcast
from django.core.validators import FileExtensionValidator


class MP3UploadForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ('title', 'file', 'cover')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
