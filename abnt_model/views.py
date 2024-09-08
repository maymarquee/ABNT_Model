from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from setup import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings

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


def redefinir_senha(request, username, token):
    usuario = User.objects.get(username=username)
    senha = request.POST.get("senha")
    confirmar_senha = request.POST.get("confirmar_senha")

    if request.method == "POST":
        if senha != confirmar_senha:
            return redirect("redefinir_senha", username, token)

        usuario.set_password(senha)
        usuario.save(force_update=True)

        return redirect("login")

    gerador = PasswordResetTokenGenerator()

    if gerador.check_token(usuario, token):

        context = {"username":username, "token":token}

        return render(request,'abnt_model/redefinir_senha.html', context)


def recuperar_conta(request):

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
                message=f"Uma requisição de redefinição de senha foi feita no site ABNT Model para a conta vinculada a este email, para prosseguir com a redefinição de senha basta acessar o seguinte link: http://127.0.0.1:8000/redefinir_senha/{username}/{token}. Caso a requisição não tenha sido feita por você por favor ignore este email.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return render(request, 'abnt_model/recuperar_conta.html',context)
        else:
            return render(request, 'abnt_model/recuperar_conta.html', context={"status_de_envio": False})

    return render(request, 'abnt_model/recuperar_conta.html', context={"status_de_envio": False})



def perfil(request):
    context = {
        "nome": request.user.first_name,
        "sobrenome": request.user.last_name,
        "email": request.user.email
    }
    return render(request, 'abnt_model/perfil.html', context)


def login_view(request):
    context = {
        "status_de_envio":False,
    }

    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        user = authenticate(username=email,password=senha)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            print('erro')
            context = {
            "status_de_envio":True,
            "mensagem": 'Senha ou email inválidos, tente novamente. *'
            }
            return render(request, 'abnt_model/login.html',context)
        
    return render(request, 'abnt_model/login.html',context)

def cadastro(request):
    context = {
        "status_de_erro":False
    }

    if request.method == "POST":

        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        if not all([nome,sobrenome,email,senha,confirmar_senha]):
            context = {
            "status_de_erro":True,
            "mensagem": 'Todos os campos devem ser preenchidos.'
            }
            return render(request, 'abnt_model/cadastro.html',context)
        
        if senha != confirmar_senha: #se tiver errada ele recarrega a pagina
            context = {
            "status_de_erro":True,
            "mensagem": 'As senhas não são iguais, é necessário que sejam iguais para prosseguir.'
            }
            return render(request, 'abnt_model/cadastro.html',context)
        
        if User.objects.filter(email=email).exists():
            context = {
            "status_de_erro":True,
            "mensagem": 'Este email já está cadastrado.'
            }
            return render(request, 'abnt_model/cadastro.html',context)
        try:
            user = User.objects.create_user(username= email, email=email, password=senha, first_name=nome ,last_name=sobrenome)
            user.save()
            return redirect('login')
        except:
            context = {
            "status_de_erro":True,
            "mensagem": 'Houve um erro no preenchimento dos campos, se atente aos dados solicitados.'
            }
            return render(request, 'abnt_model/cadastro.html',context)
    print(context)
    return render(request, 'abnt_model/cadastro.html',context)

@login_required
def deletar_conta(request):
    if request.method == "POST":
        frase = request.POST.get("frase")
        frase = frase.lower()
        print(frase)
        if  frase == "desejo excluir minha conta permanentemente":
            request.user.delete()
            return redirect('index')
        else:
            mensagem = "Não foi possível deletar a conta. Digite a frase corretamente. **"
            return render(request, 'abnt_model/deletar_conta.html', {"mensagem": mensagem})

    return render(request, 'abnt_model/deletar_conta.html')

@login_required
def formatador(request):
    if request.method == "POST":
        # Obtendo dados do formulário
        nome_do_arquivo = request.POST.get("nome_do_arquivo", "documento")

        dados = {
            'titulo': request.POST.get("titulo", ""),
            'autor': request.POST.get("autor", ""),
            'instituicao': request.POST.get("instituicao", ""),
            'ano': request.POST.get("ano", ""),
            'resumo': request.POST.get("resumo", ""),
            'palavras_chaves': request.POST.get("palavras_chaves", ""),
            'abstract': request.POST.get("abstract", ""),
            'keywords': request.POST.get("keywords", ""),
            'introducao': request.POST.get("introducao", ""),
            'problematizacao': request.POST.get("problematizacao", ""),
            'justificativa': request.POST.get("justificativa", ""),
            'questao_geral': request.POST.get("questao_geral", ""),
            'objetivo': request.POST.get("objetivo", ""),
            'metodologia': request.POST.get("metodologia", ""),
            'desenvolvimento': request.POST.get("desenvolvimento", ""),
            'analise_discussao': request.POST.get("analise_discussao", ""),
            'conclusao': request.POST.get("conclusao", ""),
            'referencias': request.POST.get("referencias", ""),
        }
        tipo_do_arquivo = request.POST.get("tipo_do_arquivo", "pdf")
        html_string = render_to_string('abnt_model/documento.html', dados)
        
        if tipo_do_arquivo == "pdf":
            # Converte o HTML para PDF
            pdf_file = HTML(string=html_string).write_pdf()
            
            # Retorna o PDF como resposta
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nome_do_arquivo}.pdf"'
            return response
        
        elif tipo_do_arquivo == "docx":
            # Converte o HTML para DOCX
            pass

    return render(request, 'abnt_model/formatador.html')


