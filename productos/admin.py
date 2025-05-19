from django.contrib import admin
from .models import Product, Container, Order, OrderDetail

admin.site.register(Product)
admin.site.register(Container)

admin.site.register(Order)
admin.site.register(OrderDetail)