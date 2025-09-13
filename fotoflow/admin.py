import os

from django.contrib import admin
from django.http import FileResponse

from .models import Cliente, Contrato, ContratoCliente, ModeloContrato, Servico, ContratoServico
from .utils import gerar_contrato

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'telefone', 'is_active', 'created_at', 'updated_at')
    search_fields = ('nome_completo',)
    list_filter = ('is_active',)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "detalhes", "descricao", "valor_formatado")
    search_fields = ("nome", "detalhes")

    def valor_formatado(self, obj):
        # obj é a instância do modelo Servico da linha atual
        if obj.valor is None:
            return "N/A"

        return locale.currency(obj.valor, symbol="", grouping=True)

    valor_formatado.short_description = "Valor (R$)"
    valor_formatado.admin_order_field = 'valor'


class ContratoClienteInline(admin.TabularInline):
    model = ContratoCliente
    extra = 1
    autocomplete_fields = ("cliente",)


class ContratoServicoInline(admin.TabularInline):
    model = ContratoServico
    extra = 1
    autocomplete_fields = ("servico",)


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "titulo", "data", "valor_formatado")
    search_fields = ("titulo", 'codigo')
    inlines = [ContratoClienteInline, ContratoServicoInline]
    actions = ["gerar_documento"]

    @admin.action(description="Gerar documento do contrato")
    def gerar_documento(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Selecione apenas 1 contrato para gerar o documento.", level="error")
            return

        contrato = queryset.first()
        path = gerar_contrato(contrato)
        return FileResponse(open(path, "rb"), as_attachment=True, filename=os.path.basename(path))

    def valor_formatado(self, obj):
        # obj é a instância do modelo Servico da linha atual
        if obj.valor is None:
            return "N/A"

        return locale.currency(obj.valor, symbol="", grouping=True)

    valor_formatado.short_description = "Valor (R$)"
    valor_formatado.admin_order_field = 'valor'

@admin.register(ModeloContrato)
class ModeloContratoAdmin(admin.ModelAdmin):
    list_display = ("nome", "arquivo")
