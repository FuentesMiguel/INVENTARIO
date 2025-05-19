# orders/views.py
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from ..models import Order
from ..forms import OrderForm, OrderDetailFormSet


# View to list orders
class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Order List'
        context['create_url'] = reverse('products:order_create')
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            orders = [order.to_json() for order in Order.objects.all()]
            return JsonResponse({'data': orders})
        except Exception as e:
            print("Error in OrderListView:", e)
            return JsonResponse({'error': str(e)}, status=500)


# View to create a new order
class OrderCreateView(SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('products:order_list')
    success_message = "Order created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderDetailFormSet(self.request.POST)
        else:
            context['formset'] = OrderDetailFormSet()
        context['title'] = 'New Order'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        try:
            if form.is_valid() and formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                messages.success(self.request, self.success_message)
                return super().form_valid(form)
            else:
                return self.form_invalid(form)
        except IntegrityError as e:
            form.add_error(None, f"Database Error: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class OrderUpdateView(SuccessMessageMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('products:order_list')
    success_message = "Order updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderDetailFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderDetailFormSet(instance=self.object)
        context['title'] = 'Edit Order'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        try:
            if form.is_valid() and formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                messages.success(self.request, self.success_message)
                return super().form_valid(form)
            else:
                return self.form_invalid(form)
        except IntegrityError as e:
            form.add_error(None, f"Database Error: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class OrderDeleteView(SuccessMessageMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('products:order_list')
    success_message = "Order deleted successfully"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': self.success_message})
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)