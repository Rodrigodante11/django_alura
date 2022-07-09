from django.shortcuts import render


def index(request):
    dados = {
        'nome_da_receitas': {
            1: 'Lasanha',
            2: 'Sopa de Legumes',
            3: 'Sorvete',
            4: 'Bolo de chocolate'
        }
    }
    return render(request, 'index.html', dados)


def receita(request):
    return render(request, 'receita.html')

