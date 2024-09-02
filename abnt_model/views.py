from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout,  update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from setup import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def index(request):
    autenticado = request.user.is_authenticated
    context={
        "autenticado":autenticado
    }
    return render(request, 'abnt_model/index.html', context)

def desconectar(request):
    autenticado = request.user.is_authenticated
    if autenticado == True:
        logout(request)
        return redirect('index')



def perfil_editar(request):
    context = {
        "nome": request.user.first_name,
        "sobrenome": request.user.last_name,
        "email": request.user.email
    }

    if request.method == "POST":
        novo_nome = request.POST.get("nome")
        novo_sobrenome = request.POST.get("sobrenome")
        novo_email = request.POST.get("email")
        nova_senha = request.POST.get("senha")
        

        if not (novo_nome and novo_sobrenome and novo_email):
            return render(request, 'abnt_model/perfil_editar.html', context)
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
            return redirect('perfil_editar')
    else:
        return render(request, 'abnt_model/perfil_editar.html', context)


def recuperar_conta(request):

    # todo: falta colocar um link na mensagem para enviar para uma pagina de redefinir senha.
    # ! fazer tratamento de erros, em caso do email não existir

    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email__exact=email).exists():
            gerador_de_token = PasswordResetTokenGenerator()
            user = User.objects.get(email=email)
            token = gerador_de_token.make_token(user)
            username = user.username
            context = {
                "status_de_envio": True,
                "username":username,
                "token":token
            }

            send_mail(
                subject="Redefinição de senha",
                message="Uma requisição de redefinição de senha foi feita no site MedConnect para a conta vinculada a este email, para prosseguir com a redefinição basta acessar o seguinte. Caso a requisição não tenha sido feita por você por favor ignore este email.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return render(request, 'abnt_model/recuperar_conta.html',context)
        else:
            return render(request, 'abnt_model/recuperar_conta.html')

    return render(request, 'abnt_model/recuperar_conta.html', context={"status_de_envio": False})



def perfil(request):
    context = {
        "nome": request.user.first_name,
        "sobrenome": request.user.last_name,
        "email": request.user.email
    }
    return render(request, 'abnt_model/perfil.html', context)


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        user = authenticate(username=email,password=senha)
        if user is not None:
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
