from django.urls import path

from fotoflow.views import DashboardView, TipoClienteListView, TipoClienteCreateView, TipoClienteUpdateView, \
    TipoClienteDeleteView, ClienteCreateView, FotoflowLoginView, FotoflowLogoutView, ClienteUpdateView, ClienteListView, \
    ClienteDeleteView

app_name = 'fotoflow'

urlpatterns = [
    # Index (acesso liberado)

    # Login e logout
    path('login/', FotoflowLoginView.as_view(), name='login'),
    path('logout/', FotoflowLogoutView.as_view(), name='logout'),

    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),

    # Tipo cliente
    path('tipocliente/', TipoClienteListView.as_view(), name='tipocliente_list'),
    path('tipocliente/add', TipoClienteCreateView.as_view(), name='tipocliente_add'),
    path('tipocliente/edit/<uuid:pk>', TipoClienteUpdateView.as_view(), name='tipocliente_edit'),
    path('tipocliente/delete/<uuid:pk>', TipoClienteDeleteView.as_view(), name='tipocliente_delete'),

    # Cliente
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/add', ClienteCreateView.as_view(), name='cliente_add'),
    path('cliente/edit/<uuid:pk>', ClienteUpdateView.as_view(), name='cliente_edit'),
    path('cliente/delete/<uuid:pk>', ClienteDeleteView.as_view(), name='cliente_delete'),
]


