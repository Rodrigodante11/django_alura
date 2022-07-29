from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from receitas.models import Receita
from django.contrib.auth.models import User
from django.contrib import auth, messages


def index(request):
    dados = {
        'receitas': Receita.objects.order_by('data_receita').filter(publicada=True)
    }
    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita': receita
    }
    return render(request, 'receitas/receita.html', receita_a_exibir)



def cria_receita(request):
    if request.method == 'POST':
        # Pegando todos os dados do template cria_receita.html
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']

        user = get_object_or_404(User, pk=request.user.id)  # pegando o usuario logado

        receita = Receita.objects.create(  # criando um objeto de receitas
            pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita
        )
        receita.save()  # Salvando o objeto no banco de dados
        return redirect('dashboard')

    else:
        return render(request, 'receitas/cria_receita.html')


def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        receita = Receita.objects.get(pk=receita_id)

        receita.nome_receita = request.POST['nome_receita']
        receita.ingredientes = request.POST['ingredientes']
        receita.modo_preparo = request.POST['modo_preparo']
        receita.tempo_preparo = request.POST['tempo_preparo']
        receita.rendimento = request.POST['rendimento']
        receita.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:  # se tiver uma foto no campo de foto
            receita.foto_receita = request.FILES['foto_receita']
        print(receita.id)

        receita.save()
        return redirect('dashboard')


def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}
    return render(request, 'receitas/edita_receita.html', receita_a_editar)
