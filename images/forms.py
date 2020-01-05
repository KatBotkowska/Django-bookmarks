from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
            #field with url hidden for users -user get picture with JavaScript, url gets as parameter
        }
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('URL address doesn\'t contain valid extension for picture. '
                                        'App accepts only jpeg and jpg. Try again')
        return url

    def save(self, force_insert=False, force_update = False, commit=True):
        #create new object, without saving
        image = super(ImageCreateForm, self).save(commit = False)
        #get url from form
        image_url = self.cleaned_data['url']
        #change image name by connecting slug with extension
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        #get picture from url
        response = request.urlopen(image_url)
        #saving image in project's folder, without saving in db
        image.image.save(image_name, ContentFile(response.read()), save = False)
        #image will be saved only when commit = True
        if commit:
            image.save()
        return image
