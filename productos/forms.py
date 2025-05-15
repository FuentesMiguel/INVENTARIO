from django.core.exceptions import ValidationError
from django import forms
from .models import Product, Container, Order, OrderDetail
from django.forms import inlineformset_factory
from django.utils import timezone


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



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'phone_number',
            'table',
            'paid',
            'payment_method',
            'mode',
            'notes',
        ]

    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_name')
        phone_number = cleaned_data.get('phone_number')
        mode = cleaned_data.get('mode')
        table = cleaned_data.get('table')
        now = timezone.now()

        # Buscar si hay una orden similar hoy del mismo cliente, modo, y mesa
        if Order.objects.filter(
            customer_name=customer_name,
            phone_number=phone_number,
            mode=mode,
            table=table,
            created_at__date=now.date()
        ).exists():
            raise forms.ValidationError("An order with these details already exists today.")
        return cleaned_data


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = [
            'product_type',
            'description',
            'quantity',
            'extra_notes',
        ]

# Formset para OrderDetail relacionado con Order
OrderDetailFormSet = inlineformset_factory(
    Order, OrderDetail,
    form=OrderDetailForm,
    extra=1,
    can_delete=True
)