from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario

def index(request):
    return render(request, 'abnt_model/index.html')

def perfil(request):
    return render(request, 'abnt_model/perfil.html')

def login(request):
    return render(request, 'abnt_model/login.html')



def cadastro(request):
    if request.method == "POST":
        novo_usuario = Usuario()
        novo_usuario.nome = request.POST.get("nome")
        novo_usuario.sobrenome = request.POST.get("sobrenome")
        novo_usuario.email = request.POST.get("email")
        novo_usuario.senha = request.POST.get("senha")
        novo_usuario.confirmar_senha = request.POST.get("confirmar_senha")

        if Usuario.senha != Usuario.confirmar_senha:
            messages.error(request,'ás senhas não coincidem.')
            print('ás senhas não coincidem.')
            return redirect('cadastro')
        else:
            novo_usuario.save()
            messages.success(request,'cadastro realizado.')
            print('cadastro realizado.')
            return redirect('index')

    return render(request, 'abnt_model/cadastro.html')
