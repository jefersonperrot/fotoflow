from django import forms
from django.urls import reverse_lazy
from .models import ContratoCliente


class ContratoClienteAdminForm(forms.ModelForm):
    class Meta:
        model = ContratoCliente
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'data-autocomplete-light-url': reverse_lazy('fotoflow:autocomplete_clientes_ativos')}),
        }
