from django.core.exceptions import ValidationError
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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Envase.objects.filter(nombre=nombre).exists():
            raise ValidationError("¡Ya existe un envase con este nombre!")
        return nombre