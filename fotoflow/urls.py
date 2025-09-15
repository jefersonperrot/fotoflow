from django.urls import path
from . import views

app_name = 'fotoflow'

urlpatterns = [
    path('autocomplete/clientes_ativos/', views.autocomplete_clientes_ativos, name='autocomplete_clientes_ativos'),
]
