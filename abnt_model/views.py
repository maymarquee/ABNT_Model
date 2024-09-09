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
from PIL import Image
import urllib.request
from .models import Image

def index(request):
    autenticado = request.user.is_authenticated
    context={
        "autenticado":autenticado
    }
    return render(request, 'abnt_model/index.html', context)

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
            context = {
            "status_de_envio":True,
            "mensagem": 'Senha ou email inválidos, tente novamente. *'
            }
            return render(request, 'abnt_model/login.html',context)
        
    return render(request, 'abnt_model/login.html',context)

@login_required
def desconectar(request):
    autenticado = request.user.is_authenticated
    if autenticado == True:
        logout(request)
        return redirect('index')

def recuperar_conta(request):
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

def redefinir_senha(request, username, token):
    usuario = User.objects.get(username=username)
    senha = request.POST.get("senha")
    confirmar_senha = request.POST.get("confirmar_senha")
    context = {
        "username":username, 
        "token":token,
        }
    
    if request.method == "POST":
        if senha != confirmar_senha:
            return render(request,'abnt_model/redefinir_senha.html', context={"mensagem":'As senhas não são iguais, tente novamente. **'})

        usuario.set_password(senha)
        usuario.save(force_update=True)

        return redirect("login")

    gerador = PasswordResetTokenGenerator()

    if gerador.check_token(usuario, token):
        return render(request,'abnt_model/redefinir_senha.html', context)

@login_required
def perfil(request):
    url = Image.objects.get(user = request.user)
    context = {
        "nome": request.user.first_name,
        "sobrenome": request.user.last_name,
        "email": request.user.email,
        "imagem": url.image
    }
    return render(request, 'abnt_model/perfil.html', context)


@login_required
def perfil_editar(request):
    url = Image.objects.get(user = request.user)
    context = {
        "nome": request.user.first_name,
        "sobrenome": request.user.last_name,
        "email": request.user.email,
        "imagem": url.image
    }

    if request.method == "POST":

        novo_nome = request.POST.get("nome")
        novo_sobrenome = request.POST.get("sobrenome")
        novo_email = request.POST.get("email")
        nova_senha = request.POST.get("senha")
        nova_imagem = request.POST.get("url_imagem")
    

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

            if nova_imagem:
                if not Image.objects.filter(user= request.user).exists():
                    campo_imagem = Image.objects.create(user=user, image=nova_imagem)
                    campo_imagem.save()
                else:
                    campo_imagem = url
                    campo_imagem.image = nova_imagem
                    campo_imagem.save()

            if nova_senha:
                # Atualiza a sessão do usuário para não invalidar a sessão atual
                update_session_auth_hash(request, user)
            
            return redirect('perfil')

        except User.DoesNotExist:
            return redirect('perfil_editar')
    else:
        return render(request, 'abnt_model/perfil_editar.html', context)

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
            imagem_padrao = 'https://static.vecteezy.com/system/resources/previews/002/275/847/original/male-avatar-profile-icon-of-smiling-caucasian-man-vector.jpg'
            url = Image.objects.create(user=user, image=imagem_padrao)
            url.save()
            return redirect('login')
        except:
            context = {
            "status_de_erro":True,
            "mensagem": 'Houve um erro no preenchimento dos campos, se atente aos dados solicitados.'
            }
            return render(request, 'abnt_model/cadastro.html',context)
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

    
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML
from pdf2docx import Converter
import io
import tempfile
import os

@login_required
def formatador(request):
    if request.method == "POST":
        nome_do_arquivo = request.POST.get("nome_do_arquivo")
        dados = {
            'nome_do_arquivo': nome_do_arquivo,
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

        # Renderiza o HTML com os dados fornecidos
        html_string = render_to_string('abnt_model/documento.html', dados)
        pdf_file = HTML(string=html_string).write_pdf()

        if tipo_do_arquivo == 'pdf':
            # Envia o arquivo PDF como resposta
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nome_do_arquivo}.pdf"'
            return response
        else:
            # Salva o PDF em um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
                temp_pdf_file.write(pdf_file)
                temp_pdf_file_path = temp_pdf_file.name
            
            # Converte o PDF para DOCX
            docx_stream = io.BytesIO()
            try:
                converter = Converter(temp_pdf_file_path)
                converter.convert(docx_stream)
            finally:
                converter.close()
            
            # Remove o arquivo PDF temporário
            os.remove(temp_pdf_file_path)
            
            # Configura o stream do DOCX
            docx_stream.seek(0)
            response = HttpResponse(docx_stream.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{nome_do_arquivo}.docx"'
            return response

    return render(request, 'abnt_model/formatador.html')