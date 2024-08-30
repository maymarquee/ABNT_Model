from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

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


def perfil(request):
    nome = request.user.first_name
    sobrenome = request.user.last_name
    email = request.user.email
    senha = request.user.password

    print(f'nome:{nome}')
    print(f'sobrenome:{sobrenome}')
    print(f'email:{email}')
    print(f'senha:{senha}')

    context = {
        "nome": nome,
        "sobrenome":sobrenome,
        "email":email,
        "senha":senha
    }

    return render(request, 'abnt_model/perfil.html',context)

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

        if senha != confirmar_senha: #se tiver errada ele recarrega a pagina
            return render(request, 'abnt_model/cadastro.html')

        user = User.objects.create_user(username= email, email=email, password=senha, first_name=nome ,last_name=sobrenome)
        user.save()
        return redirect('login')

    return render(request, 'abnt_model/cadastro.html')
