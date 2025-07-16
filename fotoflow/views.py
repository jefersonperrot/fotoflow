from datetime import date

from django.conf import settings
# from django.shortcuts import render
import json
import os
from functools import lru_cache

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from fotoflow.forms import TipoClienteForm, ClienteCadastroForm, LoginForm, ClienteEditForm
from fotoflow.models import TipoCliente, Cliente


# Login
class FotoflowLoginView(LoginView):
    template_name = 'fotoflow/login.html'
    authentication_form = LoginForm
    success_url = reverse_lazy('fotoflow:dashboard')
    redirect_authenticated_user = True


class FotoflowLogoutView(LogoutView):
    template_name = 'fotoflow/logout.html'


# Função que carrega os versículos com cache na memória
@lru_cache(maxsize=1)
def carregar_versiculos():
    caminho = os.path.join(settings.BASE_DIR, 'static', 'versiculos', 'versiculos_acf_completo.json')
    with open(caminho, encoding='utf-8') as f:
        return json.load(f)


# Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "fotoflow/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        versiculos = carregar_versiculos()
        # versiculo = random.choice(versiculos)

        hoje = date.today()
        index = hoje.timetuple().tm_yday % len(versiculos)
        versiculo = versiculos[index]

        context['versiculo'] = versiculo
        return context


# Tipo de cliente
class TipoClienteListView(LoginRequiredMixin, ListView):
    model = TipoCliente
    template_name = 'fotoflow/tipocliente/index.html'
    context_object_name = 'tipo_clientes'


class TipoClienteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'fotoflow/tipocliente/add.html'
    model = TipoCliente
    form_class = TipoClienteForm
    success_url = reverse_lazy('fotoflow:tipocliente_list')


class TipoClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoCliente
    template_name = 'fotoflow/tipocliente/edit.html'
    form_class = TipoClienteForm
    # fields = ['nome', 'situacao']
    success_url = reverse_lazy('fotoflow:tipocliente_list')


class TipoClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoCliente
    template_name = 'fotoflow/tipocliente/delete.html'
    context_object_name = 'tipo_cliente'
    success_url = reverse_lazy('fotoflow:tipocliente_list')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


# Views dos clientes
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'fotoflow/cliente/index.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


class ClienteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'fotoflow/cliente/add.html'
    model = Cliente
    form_class = ClienteCadastroForm
    success_url = reverse_lazy('fotoflow:cliente_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Atribui o usuário logado
        return super().form_valid(form)


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteEditForm
    template_name = 'fotoflow/cliente/edit.html'
    success_url = reverse_lazy('fotoflow:cliente_list')

    def get_queryset(self):
        # Garante que só clientes do usuário logado possam ser editados
        return Cliente.objects.filter(usuario=self.request.user)


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'fotoflow/cliente/delete.html'
    success_url = reverse_lazy('fotoflow:cliente_list')

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)