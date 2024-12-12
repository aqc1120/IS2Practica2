from django import forms
from .models import Cruise

class OpinionForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100)
    cruise = forms.ModelChoiceField(queryset=Cruise.objects.all(), label='Crucero')
    opinion = forms.TextField(label='Opinión')
    valoracion = forms.IntegerField(label='Valoracion')