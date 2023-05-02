from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['loc','upload','language']

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['text']
        
class AwarenessForm(forms.ModelForm):
    class Meta:
        model = Awareness
        fields = ['loc','date','event','time','file']