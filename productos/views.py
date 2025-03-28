from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto, Envase
from .forms import ProductoForm, EnvaseForm
from django.contrib.messages.views import SuccessMessageMixin

# Vista para listar los productos
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

# Vista para agregar un nuevo producto
class ProductoCreateView(SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:producto_list')
    success_message = "Producto creado exitosamente"

# Vista para editar un producto existente
class ProductoUpdateView(SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:producto_list')
    success_message = "Producto actualizado exitosamente"

# Vista para eliminar un producto
class ProductoDeleteView(SuccessMessageMixin, DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('productos:producto_list')
    success_message = "Producto eliminado exitosamente"

# Vista para listar los envases
class EnvaseListView(ListView):
    model = Envase
    template_name = 'productos/envase_list.html'
    context_object_name = 'envases'

# Vista para agregar un nuevo envase
class EnvaseCreateView(SuccessMessageMixin, CreateView):
    model = Envase
    form_class = EnvaseForm
    template_name = 'productos/envase_form.html'
    success_url = reverse_lazy('productos:envase_list')
    success_message = "Envase creado exitosamente"

# Vista para editar un envase existente
class EnvaseUpdateView(SuccessMessageMixin, UpdateView):
    model = Envase
    form_class = EnvaseForm
    template_name = 'productos/envase_form.html'
    success_url = reverse_lazy('productos:envase_list')
    success_message = "Envase actualizado exitosamente"

# Vista para eliminar un envase
class EnvaseDeleteView(SuccessMessageMixin, DeleteView):
    model = Envase
    template_name = 'productos/envase_confirm_delete.html'
    success_url = reverse_lazy('productos:envase_list')
    success_message = "Envase eliminado exitosamente"
