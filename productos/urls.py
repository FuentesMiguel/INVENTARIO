from django.urls import path
from .views import order_views, product_views, containers_views, views

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # Página principal (Dashboard)

    path('product/', product_views.ProductListView.as_view(), name='product_list'),
    path('product/new/', product_views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', product_views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', product_views.ProductDeleteView.as_view(), name='product_delete'),

    path('containers/', containers_views.ContainerListView.as_view(), name='container_list'),
    path('container/new/', containers_views.ContainerCreateView.as_view(), name='container_create'),
    path('container/<int:pk>/edit/', containers_views.ContainerUpdateView.as_view(), name='container_update'),
    path('container/<int:pk>/delete/', containers_views.ContainerDeleteView.as_view(), name='container_delete'),

    path('orders/', order_views.OrderListView.as_view(), name='order_list'),
    path('orders/new/', order_views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', order_views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', order_views.OrderDeleteView.as_view(), name='order_delete'),
]
