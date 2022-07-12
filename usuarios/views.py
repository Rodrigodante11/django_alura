from django.shortcuts import render


def cadastro(request):
    return render(request, 'usuarios/cadastro.html')


def login(request):
    return render(request, 'usuarios/login.html')


def logout(request):
    return render(request, 'usuarios/logout.html')


def dashboard(request):
    return render(request, 'usuarios/dashboard.html')
