from django.core.exceptions import ValidationError
from django import forms
from .models import Product, Container

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'container', 'quantity', 'net_weight']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'container': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ['name', 'weight']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Container.objects.filter(name=name).exists():
            raise ValidationError("A container with this name already exists!")
        return name
