import os

from django.contrib import admin
from django.http import FileResponse

from .models import Cliente, Contrato, ContratoCliente, ModeloContrato, Servico, ContratoServico
from .utils import gerar_contrato

from .forms import ContratoClienteAdminForm

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class BaseUserAdmin(admin.ModelAdmin):
    exclude = ("usuario",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)


@admin.register(Cliente)
class ClienteAdmin(BaseUserAdmin):
    list_display = ('nome_completo', 'telefone', 'is_active', 'created_at', 'updated_at')
    search_fields = ('nome_completo',)
    list_filter = ('is_active',)


@admin.register(Servico)
class ServicoAdmin(BaseUserAdmin):
    list_display = ("nome", "detalhes", "descricao", "valor_formatado")
    search_fields = ("nome", "detalhes")

    def valor_formatado(self, obj):
        if obj.valor is None:
            return "N/A"

        return locale.currency(obj.valor, symbol=False, grouping=True)

    valor_formatado.short_description = "Valor (R$)"
    valor_formatado.admin_order_field = 'valor'

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)
    #     if hasattr(Servico, 'is_active'):
    #         queryset = queryset.filter(is_active=True)
    #     return queryset, use_distinct


class ContratoClienteInline(admin.TabularInline):
    model = ContratoCliente
    extra = 1
    form = ContratoClienteAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cliente" and not request.user.is_superuser:
            kwargs["queryset"] = Cliente.objects.filter(usuario=request.user, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ContratoServicoInline(admin.TabularInline):
    model = ContratoServico
    extra = 1
    autocomplete_fields = ("servico",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "servico" and not request.user.is_superuser:
            kwargs["queryset"] = Servico.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Contrato)
class ContratoAdmin(BaseUserAdmin):
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

        if not contrato.modelo:
            self.message_user(
                request,
                f"Erro ao gerar documento: o contrato '{contrato}' não possui um modelo de contrato associado.",
                level="error"
            )
            return

        try:
            path = gerar_contrato(contrato)
            return FileResponse(open(path, "rb"), as_attachment=True, filename=os.path.basename(path))
        except Exception as e:
            self.message_user(
                request,
                f"Ocorreu um erro inesperado ao gerar o documento: {e}",
                level="error"
            )
            return

        # contrato = queryset.first()
        # path = gerar_contrato(contrato)
        # return FileResponse(open(path, "rb"), as_attachment=True, filename=os.path.basename(path))

    def valor_formatado(self, obj):
        # obj é a instância do modelo Servico da linha atual
        if obj.valor is None:
            return "N/A"

        return locale.currency(obj.valor, symbol=False, grouping=True)

    valor_formatado.short_description = "Valor (R$)"
    valor_formatado.admin_order_field = 'valor'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "modelo" and not request.user.is_superuser:
            kwargs["queryset"] = ModeloContrato.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# @admin.register(ContratoCliente)
class ContratoClienteAdmin(BaseUserAdmin):
    list_display = ("contrato", "cliente", "papel")
    search_fields = ("contrato__titulo", "cliente__nome_completo")


# @admin.register(ContratoServico)
class ContratoServicoAdmin(BaseUserAdmin):
    list_display = ("contrato", "servico")
    search_fields = ("contrato__titulo", "servico__nome")


@admin.register(ModeloContrato)
class ModeloContratoAdmin(BaseUserAdmin):
    list_display = ("nome", "arquivo")
    search_fields = ("nome",)
