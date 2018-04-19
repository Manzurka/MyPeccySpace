from django import forms
from models import *


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class FileUploadForm(forms.Form):
    """File upload form."""
    upload = forms.FileField()