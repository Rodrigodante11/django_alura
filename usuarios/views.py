from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # trazendo os modelos ja cadastrados


def cadastro(request):
    if request.method == 'POST':  # Olhe a pagina cadastro.html  27:  <form action="{% url 'cadastro' %}" method="POST">
        # print('Eh methodo POST Usuario criado com sucesso')
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        # print(nome, email, senha , senha2)

        if not nome.strip():
            print('O campo nome nao pode ficar em branco')  # so deu espaco no campo nome
            return redirect('cadastro')

        if not email.strip():
            print('O campo email nao pode ficar em branco')  # so deu espaco no email nome
            return redirect('cadastro')

        if senha != senha2:
            print('As senhas nao sao iguais')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            print('Usuario ja cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)  # criando um objeto do usuario
        user.save()  # salvando o usuario na base de dados
        print('Usuario cadastrado com sucesso')

        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    return render(request, 'usuarios/login.html')


def logout(request):
    return render(request, 'usuarios/logout.html')


def dashboard(request):
    return render(request, 'usuarios/dashboard.html')
