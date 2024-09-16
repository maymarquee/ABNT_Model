# urls.py
from django.urls import path
from . import views  # Importa a views onde tem os controladores


urlpatterns = [
    path("", views.index, name="index"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/editar", views.perfil_editar, name="perfil_editar"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.desconectar, name="desconectar"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("recuperar_conta/", views.recuperar_conta, name="recuperar_conta"),
    path("redefinir_senha/<str:username>/<str:token>", views.redefinir_senha, name="redefinir_senha"),
    path("deletar_conta/", views.deletar_conta, name="deletar_conta"),
    path("formatador/<int:pk>", views.formatador, name="formatador"),
    path("formatador/", views.formatador, name="formatador"),
    path("documentos_salvos/", views.documentos_salvos, name="documentos_salvos"),
]

