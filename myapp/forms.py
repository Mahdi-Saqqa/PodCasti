from django import forms
from .models import Podcast

class MP3UploadForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ('title','file','cover','duration')

class MyForm(forms.Form):
    mp3_file = forms.FileField(label='Choose an MP3 file', help_text='Max. 10 MB')
    image_file = forms.FileField(label='Choose an image file', help_text='Max. 5 MB')

    def clean_mp3_file(self):
        mp3_file = self.cleaned_data.get('mp3_file')
        if mp3_file:
            if mp3_file.size > 10000000:
                raise forms.ValidationError('The MP3 file is too large.')
            if not mp3_file.name.endswith('.mp3'):
                raise forms.ValidationError('Only MP3 files are allowed.')
        return mp3_file

    def clean_image_file(self):
        image_file = self.cleaned_data.get('image_file')
        if image_file:
            if image_file.size > 5000000:
                raise forms.ValidationError('The image file is too large.')
            if not image_file.name.endswith('.jpg') and not image_file.name.endswith('.jpeg') and not image_file.name.endswith('.png'):
                raise forms.ValidationError('Only JPG, JPEG, and PNG files are allowed.')
        return image_file