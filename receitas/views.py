from django.shortcuts import render
from .models import Receita


def index(request):
    dados = {
        'receitas': Receita.objects.all()
    }
    return render(request, 'index.html', dados)


def receita(request):
    return render(request, 'receita.html')
