from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # trazendo os modelos ja cadastrados
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    if request.method == 'POST':  # Olhe a pagina cadastro.html  27:  <form action="{% url 'cadastro' %}" method="POST">
        # print('Eh methodo POST Usuario criado com sucesso')
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        # print(nome, email, senha , senha2)

        if campo_vazio(nome):
            messages.error(request, 'O campo nome nao pode ficar em branco')  # so deu espaco no campo nome
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'O campo email nao pode ficar em branco')  # so deu espaco no email nome
            return redirect('cadastro')

        if senha != senha2:
            messages.error(request, 'As senhas nao sao iguais')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():  # Verificando se o email existe na base de dados
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():  # Verificando se o email existe na base de dados
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)  # criando um objeto do usuario
        user.save()  # salvando o usuario na base de dados

        messages.success(request, 'Usuario cadastrado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':  # Olhe a pagina login.html  27:   <form action="{%  url 'login' %}" method="POST">
        email = request.POST['email']  # ['email'] == campo name=`email` da tag <input>
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'O campo email e senha nao pode ser vazio')
            return redirect('login')

        if User.objects.filter(email=email).exists():  # Verificando se o email existe na base de dados
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()  # pegando o username

            user = auth.authenticate(request, username=nome, password=senha)  # autenticando o usuario

            if user is not None:
                auth.login(request, user)
                print('login Sucesso')
                return redirect('dashboard')

    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:  # Para se exibir a dashboard.html se estiver um usuario logado
        id = request.user.id

        # enviando as receitas por filtro do usuario logado
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas':receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


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


def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}
    return render(request, 'receitas/edita_receita.html', receita_a_editar)


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


def campo_vazio(campo):
    return not campo.strip()
