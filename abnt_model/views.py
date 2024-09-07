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


from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch

def formatador(request):
    if request.method == "POST":
        # Obtendo dados do formulário
        titulo = 'O PODER DAS REDES SOCIAIS NA FORMAÇÃO DA OPINIÃO PÚBLICA'  
        autor = 'Caio Ferreira Duarte'
        instituicao = 'Universidade de Brasília'
        ano = '2024'
        resumo = 'Com a revolução digital, conhecida popularmente como terceira revolução industrial, entre os anos de 1950 e 1970, a era digital se solidificou cada vez mais com o avanço tecnológico, tornando-o globalizado, conectando pessoas e formando opiniões, este ensaio então visa dialogar com a opinião pública da socióloga turca, Zeynep Tufekci, examinando como as redes sociais moldam as percepções e decisões de um indivíduo, sendo este um tema relevante devido sua modernidade à era contemporânea, aonde de acordo com o Relatório Estado da Banda Larga no Mundo 2023 da União Internacional de Telecomunicações (UIT) (2023), cerca de 67 da população está conectada a internet, tendo total chance de ser influenciada pela mesma.'
        palavras_chaves = 'redes sociais, fake news, regulamentação, opinião pública'
        abstract = 'Com a revolução digital, conhecida popularmente como terceira revolução industrial, entre os anos de 1950 e 1970, a era digital se solidificou cada vez mais com o avanço tecnológico, tornando-o globalizado, conectando pessoas e formando opiniões, este ensaio então visa dialogar com a opinião pública da socióloga turca, Zeynep Tufekci, examinando como as redes sociais moldam as percepções e decisões de um indivíduo, sendo este um tema relevante devido sua modernidade à era contemporânea, aonde de acordo com o Relatório Estado da Banda Larga no Mundo 2023 da União Internacional de Telecomunicações (UIT) (2023), cerca de 67 da população está conectada a internet, tendo total chance de ser influenciada pela mesma.'
        keywords =  'redes sociais, fake news, regulamentação, opinião pública'
        introducao = 'A ascensão das redes sociais transformou radicalmente a maneira como as informações são compartilhadas e consumidas, tornando-se uma força crucial na formação da opinião pública. Este fenômeno é amplamente discutido por Zeynep Tufekci, cuja pesquisa oferece uma visão crítica sobre a interseção entre tecnologia digital e sociedade. Tufekci explora como as redes sociais não apenas facilitam a comunicação, mas também moldam e, em muitos casos, distorcem as percepções individuais e coletivas. Um dos aspectos mais preocupantes desse impacto é a disseminação de fake news e desinformação, um tema central em suas análises. No contexto digital atual, a facilidade com que informações são propagadas nas redes sociais trouxe à tona um desafio significativo: a proliferação de notícias falsas e informações enganosas. Tufekci argumenta que, enquanto as redes sociais democratizam o acesso à informação, elas também criam um ambiente propício para a disseminação de desinformação. A velocidade e a escala com que essas informações podem ser compartilhadas amplificam seu impacto, muitas vezes superando a capacidade dos indivíduos e das instituições de verificar a veracidade do conteúdo. Neste texto, exploraremos como as redes sociais se tornaram um terreno fértil para a disseminação de fake news, examinando os mecanismos que facilitam essa propagação e os impactos resultantes na formação da opinião pública. A discussão se baseará nas ideias de Zeynep Tufekci, analisando a interseção entre tecnologia e desinformação e refletindo sobre possíveis abordagens para mitigar os efeitos negativos dessa dinâmica na sociedade contemporânea.'
        desenvolvimento = request.POST.get("desenvolvimento")
        conclusao = request.POST.get("conclusao")
        referencias = request.POST.get("referencias")
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        
        estilo_titulo = ParagraphStyle(name='Title', fontName='Times-Bold', fontSize=14, alignment=1, spaceAfter=12)
        estilo_subtitulo = ParagraphStyle(name='Subtitle', fontName='Times-Bold', fontSize=14, spaceAfter=6)
        estilo_normal = ParagraphStyle(name='Normal', fontName='Times-Roman', fontSize=12, leading=14)
        estilo_normal_centralizado = ParagraphStyle(name='Normal_centralizado', fontName='Times-Roman', fontSize=12, leading=14, alignment=1)
        conteudo = []

        # Capa
        conteudo.append(Paragraph(instituicao, estilo_normal))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(autor, estilo_normal_centralizado))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(titulo, estilo_titulo))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(regiao, estilo_normal))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(ano, estilo_normal))
        conteudo.append(PageBreak())
        
        # Resumo e Palavras-Chaves
        conteudo.append(Paragraph("Resumo", estilo_subtitulo))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(resumo, estilo_normal))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(f"Palavras-Chaves: {palavras_chaves}", estilo_normal))
        conteudo.append(PageBreak())

        # Abstract e Keywords
        conteudo.append(Paragraph("Abstract", estilo_subtitulo))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(abstract, estilo_normal))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(f"Keywords: {keywords}", estilo_normal))
        conteudo.append(PageBreak())
        
        # Sumário
        toc = []
        toc.append(Paragraph("Sumário", estilo_titulo))
        toc.append(Spacer(1, 12))
        toc.append(Paragraph("1. Introdução", estilo_normal))
        toc.append(Paragraph("2. Desenvolvimento", estilo_normal))
        toc.append(Paragraph("3. Conclusão", estilo_normal))
        toc.append(Paragraph("4. Referências Bibliográficas", estilo_normal))
        toc.append(PageBreak())

        # Adiciona o Sumário ao início do documento
        conteudo.insert(0, Paragraph("Sumário", estilo_titulo))
        conteudo.insert(1, Spacer(1, 12))
        conteudo.extend(toc)
        conteudo.append(PageBreak())
        
        # Introdução
        conteudo.append(Paragraph("1. Introdução", estilo_subtitulo))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(introducao, estilo_normal))
        conteudo.append(PageBreak())
        
        # Desenvolvimento
        conteudo.append(Paragraph("2. Desenvolvimento", estilo_subtitulo))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(desenvolvimento, estilo_normal))
        conteudo.append(PageBreak())
        
        # Conclusão
        conteudo.append(Paragraph("3. Conclusão", estilo_subtitulo))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(conclusao, estilo_normal))
        conteudo.append(PageBreak())
        
        # Referências
        conteudo.append(Paragraph("Referências", estilo_subtitulo))
        conteudo.append(Spacer(1, 12))
        conteudo.append(Paragraph(referencias, estilo_normal))
        
        # Adiciona números de páginas
        def add_page_numbers(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.drawString(7.5 * inch, 0.75 * inch, f"Página {canvas.getPageNumber()}")
            canvas.restoreState()

        doc.build(conteudo, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)

        # Rewind the buffer to the beginning
        buffer.seek(0)

        # Create the HTTP response with the PDF file
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="documento.pdf"'
        
        return response

    return render(request, 'abnt_model/formatador.html')