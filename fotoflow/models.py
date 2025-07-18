import uuid
from django.db import models
from django.contrib.auth.models import User


class TipoCliente(models.Model):
    SITUACAO = [
        (0, 'Inativo'),
        (1, 'Ativo')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=50)
    situacao = models.IntegerField(choices=SITUACAO, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


# Create your models here.
class Cliente(models.Model):
    TIPO_PESSOA = [
        (1, 'Física'),
        (2, 'Jurídica')
    ]
    SITUACAO = [
        (0, 'Inativo'),
        (1, 'Ativo')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pessoa = models.IntegerField(choices=TIPO_PESSOA, default='1')
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    rg = models.CharField(max_length=15, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100)
    celular = models.CharField(max_length=20)
    endereco_completo = models.CharField(max_length=255, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    chave_acesso = models.CharField(max_length=50, blank=True, null=True)
    senha_acesso = models.CharField(max_length=50, blank=True, null=True)
    situacao = models.IntegerField(choices=SITUACAO, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_completo


# Responsavel por criar um token publico, que será enviado para o cliente
class TokenPublico(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.token}"


class TipoTrabalho(models.Model):
    SITUACAO = [
        (0, 'Inativo'),
        (1, 'Ativo')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    nome_controle = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    situacao = models.IntegerField(choices=SITUACAO, default='1')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome