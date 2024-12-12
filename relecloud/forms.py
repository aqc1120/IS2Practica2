from django import forms
from .models import Cruise

class OpinionForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cruise = forms.ModelChoiceField(queryset=Cruise.objects.all(), label='Crucero', widget=forms.Select(attrs={'class': 'form-control'}))
    opinion = forms.CharField(label='Opinión', widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'form-control'}))
    valoracion = forms.IntegerField(label='valoracion', widget=forms.NumberInput(attrs={'class': 'form-control'}))