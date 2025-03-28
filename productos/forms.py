from django import forms
from .models import Producto, Envase

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'envase', 'cantidad', 'peso_neto']
        widgets = {
            'envase': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EnvaseForm(forms.ModelForm):
    class Meta:
        model = Envase
        fields = ['nombre', 'peso']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
        }
