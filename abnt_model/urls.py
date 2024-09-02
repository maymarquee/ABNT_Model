from django.urls import path

from . import views #importar views, onde fica a lógica

#aqui são as rotas da aplicação 'abnt_model'

urlpatterns = [
    path("", views.index, name="index"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/editar", views.perfil_editar, name="perfil_editar"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.desconectar, name="desconectar"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("recuperar_conta/", views.recuperar_conta, name="recuperar_conta")
]