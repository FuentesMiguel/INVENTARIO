from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Product, Container
from .forms import ProductForm, ContainerForm

# View to list products
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse('products:product_create')
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            products = [product.to_json() for product in Product.objects.all()]
            return JsonResponse({'data': products})
        except Exception as e:
            print("Error en vista ProductListView:", e)
            return JsonResponse({'error': str(e)}, status=500)

# View to create a new product
class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    success_message = "Product created successfully"


# View to update an existing product
class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    success_message = "Product updated successfully"


# View to delete a product
class ProductDeleteView(SuccessMessageMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')
    success_message = "Product deleted successfully"


# View to list containers
class ContainerListView(SuccessMessageMixin, ListView):
    model = Container
    template_name = 'products/container_list.html'
    context_object_name = 'containers'


# View to create a new container
class ContainerCreateView(CreateView):
    model = Container
    form_class = ContainerForm
    template_name = 'products/container_form.html'
    success_url = reverse_lazy('products:container_list')
    success_message = "Container created successfully"

    def form_valid(self, form):
        try:
            self.object = form.save()
            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        except IntegrityError as e:
            messages.error(self.request, f"An error occurred while saving the container: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was a problem with the form. Please check the fields.")
        return super().form_invalid(form)


# View to update an existing container
class ContainerUpdateView(SuccessMessageMixin, UpdateView):
    model = Container
    form_class = ContainerForm
    template_name = 'products/container_form.html'
    success_url = reverse_lazy('products:container_list')
    success_message = "Container updated successfully"


# View to delete a container
class ContainerDeleteView(SuccessMessageMixin, DeleteView):
    model = Container
    template_name = 'products/container_confirm_delete.html'
    success_url = reverse_lazy('products:container_list')
    success_message = "Container deleted successfully"
