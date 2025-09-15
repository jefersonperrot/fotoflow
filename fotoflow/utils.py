import os
from django.conf import settings
from docxtpl import DocxTemplate


def gerar_contrato(contrato):
    modelo_path = contrato.modelo.arquivo.path
    doc = DocxTemplate(modelo_path)

    # clientes
    clientes_formatados = []
    for cc in contrato.participantes.all():
        c = cc.cliente
        partes = []

        partes.append(f"{c.nome_completo}")

        if c.nacionalidade:
            partes.append(c.nacionalidade)

        if c.data_nascimento:
            partes.append(f"nascido(a) em {c.data_nascimento.strftime('%d/%m/%Y')}")

        if c.endereco_completo:
            partes.append(f"residente a {c.endereco_completo}")

        if c.cpf_cnpj:
            partes.append(f"CPF nº {c.cpf_cnpj}")

        if c.rg_ie:
            partes.append(f"RG nº {c.rg_ie}")

        if c.telefone:
            partes.append(f"celular {c.telefone}")

        if c.email:
            partes.append(f"e-mail {c.email}")

        clientes_formatados.append(", ".join(partes))

    dados_clientes = " e ".join(clientes_formatados)

    # servicos
    # Monta a lista de clientes formatados
    servicos_formatados = []
    for servicos in contrato.servicos.all():
        s = servicos.servico
        jobs = []

        jobs.append(s.descricao)

        servicos_formatados.append(", ".join(jobs))

    dados_servicos = "\n\n".join(servicos_formatados)

    meses = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro",
    }

    # Monta o contexto
    context = {
        "clientes": ", ".join([cc.cliente.nome_completo for cc in contrato.participantes.all()]),
        "valor": f"R$ {contrato.valor:,.2f}",
        "data": contrato.data.strftime("%d/%m/%Y"),
        "data_extenso": f"{contrato.data.day:02d} de {meses[contrato.data.month]} de {contrato.data.year}",
        "dados_clientes": dados_clientes,
        "dados_servicos": dados_servicos,
    }

    doc.render(context)

    output_dir = os.path.join(settings.MEDIA_ROOT, "files/contratos_gerados")
    os.makedirs(output_dir, exist_ok=True)

    # Define nome do arquivo
    if contrato.codigo and contrato.titulo:
        filename = f"{contrato.codigo}_{contrato.titulo}.docx"
    else:
        filename = f"contrato_{contrato.id}.docx"

    # Remove espaços e caracteres problemáticos do filename
    filename = filename.replace(" ", "_").replace("/", "-")

    output_path = os.path.join(output_dir, filename)
    doc.save(output_path)

    return output_path
