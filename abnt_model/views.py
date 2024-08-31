from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    autenticado = request.user.is_authenticated
    print(f'autenticado:{autenticado}')
    context={
        "autenticado":autenticado
    }
    return render(request, 'abnt_model/index.html', context)

def desconectar(request):
    autenticado = request.user.is_authenticated
    if autenticado == True:
        logout(request)
        return redirect('index')

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

def perfil_editar(request):
    if request.method == "POST":
        novo_nome = request.POST.get("nome")
        novo_sobrenome = request.POST.get("sobrenome")
        novo_email = request.POST.get("email")
        nova_senha = request.POST.get("senha")
        
        if not (novo_nome and novo_sobrenome and novo_email):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'abnt_model/perfil_editar.html', context={
                "nome": request.user.first_name,
                "sobrenome": request.user.last_name,
                "email": request.user.email
            })

        try:
            user = User.objects.get(email=request.user.email)
            user.first_name = novo_nome
            user.last_name = novo_sobrenome
            user.email = novo_email
            if nova_senha:
                user.set_password(nova_senha)
            user.save()
            
            if nova_senha:
                # Atualiza a sessão do usuário para não invalidar a sessão atual
                update_session_auth_hash(request, user)
            
            return redirect('perfil')

        except User.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return redirect('perfil_editar')

    else:
        context = {
            "nome": request.user.first_name,
            "sobrenome": request.user.last_name,
            "email": request.user.email
        }
        return render(request, 'abnt_model/perfil_editar.html', context)

def perfil(request):
    context = {
        "nome": request.user.first_name,
        "sobrenome": request.user.last_name,
        "email": request.user.email
    }
    return render(request, 'abnt_model/perfil.html', context)


def login_view(request):
    print('teste')
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        user = authenticate(username=email,password=senha)
        print('O POST FUNCIONOU EM LOGIN')
        print(user)
        if user is not None:
            print('logado')
            login(request,user)
            return redirect('index')
        else:
            return render(request, 'abnt_model/login.html')
        
    return render(request, 'abnt_model/login.html')

def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        if not all([nome,sobrenome,email,senha,confirmar_senha]):
            # ! tem q ter pop-up de erro pra qnd ja existir email
            return render(request, 'abnt_model/cadastro.html')
        if senha != confirmar_senha: #se tiver errada ele recarrega a pagina
            # ! tem q ter pop-up de erro pra qnd as senhas forem diferentes
            return render(request, 'abnt_model/cadastro.html')
        if User.objects.filter(email=email).exists():
            # ! tem q ter pop-up de erro pra qnd ja existir email
            return render(request, 'abnt_model/cadastro.html')
        try:
            user = User.objects.create_user(username= email, email=email, password=senha, first_name=nome ,last_name=sobrenome)
            user.save()
            return redirect('login')
        except:
            # ! tem q ter pop-up generico indicando como o usuario deve preencher os campos
            return render(request, 'abnt_model/cadastro.html')
        
    return render(request, 'abnt_model/cadastro.html')
