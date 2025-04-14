from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('containers/', views.ContainerListView.as_view(), name='container_list'),
    path('container/new/', views.ContainerCreateView.as_view(), name='container_create'),
    path('container/<int:pk>/edit/', views.ContainerUpdateView.as_view(), name='container_update'),
    path('container/<int:pk>/delete/', views.ContainerDeleteView.as_view(), name='container_delete'),
]
