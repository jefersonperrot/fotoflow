from datetime import date

from django.conf import settings
# from django.shortcuts import render
import json
import os
from functools import lru_cache

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from fotoflow.forms import TipoClienteForm, ClienteCadastroForm, LoginForm, ClienteEditForm, ClienteCadastroPublicoForm, \
    ClienteSearchForm
from fotoflow.models import TipoCliente, Cliente, TokenPublico


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
        queryset = Cliente.objects.filter(usuario=self.request.user)
        form = ClienteSearchForm(self.request.GET)

        if form.is_valid():
            termo = form.cleaned_data.get('busca')
            if termo:
                queryset = queryset.filter(
                    Q(nome_completo__icontains=termo) |
                    Q(email__icontains=termo) |
                    Q(celular__icontains=termo) |
                    Q(cpf__icontains=termo) |
                    Q(cnpj__icontains=termo)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClienteSearchForm(self.request.GET)
        return context


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


# Cadastro público de clientes
# Não precisa de login
def cadastro_publico(request, token):
    token_obj = get_object_or_404(TokenPublico, token=token)

    if request.method == 'POST':
        form_noiva = ClienteCadastroPublicoForm(request.POST, prefix='noiva')
        form_noivo = ClienteCadastroPublicoForm(request.POST, prefix='noivo')

        if form_noiva.is_valid() and form_noivo.is_valid():

            tipo_noiva_padrao = TipoCliente.objects.get(nome='Noiva')
            tipo_noivo_padrao = TipoCliente.objects.get(nome='Noivo')

            cliente_noiva = form_noiva.save(commit=False)
            cliente_noiva.usuario = token_obj.usuario
            cliente_noiva.tipo_cliente = tipo_noiva_padrao
            cliente_noiva.save()

            cliente_noivo = form_noivo.save(commit=False)
            cliente_noivo.usuario = token_obj.usuario
            cliente_noivo.tipo_cliente = tipo_noivo_padrao
            cliente_noivo.save()

            return render(request, 'fotoflow/cliente/add_success.html')

    else:
        form_noiva = ClienteCadastroPublicoForm(prefix='noiva')
        form_noivo = ClienteCadastroPublicoForm(prefix='noivo')

    return render(request, 'fotoflow/cliente/add_public.html', {
        'form_noiva': form_noiva,
        'form_noivo': form_noivo,
    })


def gerar_token_publico(request):
    token_obj = TokenPublico.objects.create(usuario=request.user)
    link = request.build_absolute_uri(f'/cadastro_cliente/{token_obj.token}/')
    return render(request, 'fotoflow/cliente/link_cadastro.html', {'link': link})

