from django import forms
from .models import Podcast

class MP3UploadForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ('title','file','cover','duration')
