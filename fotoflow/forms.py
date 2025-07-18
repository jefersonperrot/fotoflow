from django import forms
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User

from fotoflow.models import TipoCliente, Cliente, TipoTrabalho


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="E-mail ou usuário",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )


class TipoClienteForm(forms.ModelForm):
    class Meta:
        model = TipoCliente
        fields = ['nome', 'situacao']
        labels = {
            'nome': 'Tipo',
            'situacao': 'Situação',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            # 'campo2': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ClienteCadastroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_pessoa', 'tipo_cliente', 'nome_completo', 'cpf', 'rg', 'cnpj', 'razao_social',
            'email', 'celular', 'endereco_completo', 'observacoes',
        ]
        labels = {
            'nome_completo': 'Nome completo',
            'tipo_pessoa': 'Tipo do cliente',
            'razao_social': 'Razão Social',
            'observacoes': 'Observações',
            'endereco_completo': 'Endereço completo',
        }
        widgets = {
            'tipo_pessoa': forms.Select(attrs={'class': 'form-select'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-select'}),
        }
        exclude = ['usuario']


class ClienteEditForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_pessoa', 'situacao', 'tipo_cliente', 'nome_completo', 'cpf', 'rg', 'cnpj', 'razao_social',
            'email', 'celular', 'endereco_completo', 'observacoes',
        ]
        labels = {
            'nome_completo': 'Nome completo',
            'tipo_pessoa': 'Tipo do cliente',
            'razao_social': 'Razão Social',
            'observacoes': 'Observações',
            'endereco_completo': 'Endereço completo',
            'situacao': 'Situação',
        }
        widgets = {
            'tipo_pessoa': forms.Select(attrs={'class': 'form-select'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-select'}),
        }
        exclude = ['usuario']


class ClienteCadastroPublicoForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome_completo', 'cpf', 'rg',
            'email', 'celular', 'endereco_completo',
        ]
        labels = {
            'nome_completo': 'Nome',
            'cpf': 'CPF',
            'rg': 'RG',
            'razao_social': 'Razão Social',
            'observacoes': 'Observações',
            'endereco_completo': 'Endereço completo',
        }
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco_completo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['usuario', 'tipo_cliente']


class ClienteSearchForm(forms.Form):
    busca = forms.CharField(
        label='Buscar cliente',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0 shadow-none ps-1 ps-sm-2 d-md-block d-none',
            'placeholder': 'Informe Nome, e-mail, celular, CPF ou CNPJ',
            'aria-label': 'Informe Nome, e-mail, celular, CPF ou CNPJ',
        })
    )


class TipoTrabalhoForm(forms.ModelForm):
    class Meta:
        model = TipoTrabalho
        fields = ['nome', 'descricao', 'valor', 'situacao']
        labels = {
            'situacao': 'Situação',
            'descricao': 'Descrição',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'valor': forms.TextInput(attrs={'class': 'form-control mask-money'}),
        }