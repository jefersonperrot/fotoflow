from django.db import models
from django.conf import settings


class Cliente(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clientes",
        null=True, blank=True
    )
    PESSOA_FISICA = 1
    PESSOA_JURIDICA = 2
    TIPO_PESSOA_CHOICES = (
        (PESSOA_FISICA, "Pessoa Física"),
        (PESSOA_JURIDICA, "Pessoa Jurídica"),
    )

    # tipo_pessoa = models.IntegerField(choices=TIPO_PESSOA_CHOICES, verbose_name='PF/PJ')
    nome_completo = models.CharField(max_length=150, verbose_name='Nome')
    cpf_cnpj = models.CharField(max_length=50, verbose_name='CPF/CNPJ')
    rg_ie = models.CharField(max_length=50, null=True, blank=True, verbose_name='RG/IE')
    data_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de nascimento')
    nacionalidade = models.CharField(max_length=50,null=True, blank=True,  verbose_name='Nacionalidade')
    telefone = models.CharField(max_length=50, blank=True, verbose_name='Telefone(s)')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    endereco_completo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Endereço completo')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return self.nome_completo

    class Meta:
        ordering = ['nome_completo']
        verbose_name = 'Cliente'


class ModeloContrato(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="modelos_contrato",
        null=True, blank=True
    )
    nome = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to="files/modelos_contrato/")
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return self.nome


class Contrato(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contratos",
        null=True, blank=True
    )
    codigo = models.CharField(max_length=200)
    titulo = models.CharField(max_length=200)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    modelo = models.ForeignKey(ModeloContrato, on_delete=models.SET_NULL, null=True, related_name="contratos")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f"{self.codigo} - {self.titulo} - {self.data}"


class ContratoCliente(models.Model):
    PAPEL_CHOICES = [
        ("noivo", "Noivo"),
        ("noiva", "Noiva"),
        ("responsavel", "Responsável Financeiro"),
        ("testemunha", "Testemunha"),
    ]

    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True, related_name="participantes")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="contratos_participados")
    papel = models.CharField(max_length=50, choices=PAPEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        unique_together = ("contrato", "cliente", "papel")  # evita duplicidade

    def __str__(self):
        return f"{self.cliente.nome_completo} ({self.get_papel_display()})"


class Servico(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="servicos",
        null=True, blank=True
    )
    nome = models.CharField(max_length=100, verbose_name='Nome')
    detalhes = models.CharField(max_length=150, null=True, blank=True, verbose_name='Detalhes')
    descricao = models.CharField(max_length=300, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f"{self.nome} - {self.detalhes}"

    class Meta:
        ordering = ['nome']
        verbose_name = 'Serviço'


class ContratoServico(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True, related_name="servicos")
    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True, related_name="contratos_servicos")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        unique_together = ("contrato", "servico")  # evita duplicidade

    def __str__(self):
        return f"{self.servico.nome}"