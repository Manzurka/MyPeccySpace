from django import forms
from models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'location','skill', 'image')
