from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('producto/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('producto/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    path('envases/', views.EnvaseListView.as_view(), name='envase_list'),
    path('envase/nuevo/', views.EnvaseCreateView.as_view(), name='envase_create'),
    path('envase/<int:pk>/editar/', views.EnvaseUpdateView.as_view(), name='envase_update'),
    path('envase/<int:pk>/eliminar/', views.EnvaseDeleteView.as_view(), name='envase_delete'),
]
