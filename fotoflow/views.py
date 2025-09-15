from django.http import JsonResponse
from django.db.models import Q
from .models import Cliente


def autocomplete_clientes_ativos(request):
    search_term = request.GET.get('q', '')
    clientes = Cliente.objects.filter(is_active=True)

    print(request)

    if search_term:
        clientes = clientes.filter(Q(nome_completo__icontains=search_term) | Q(telefone__icontains=search_term))

    results = []
    for cliente in clientes[:10]:  # Limitar a 10 resultados para performance
        results.append({'id': cliente.pk, 'text': str(cliente)})

    return JsonResponse({'results': results})
