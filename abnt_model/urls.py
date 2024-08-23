from django.urls import path

from . import views #importar views, onde fica a lógica

#aqui são as rotas da aplicação 'abnt_model'

urlpatterns = [
    path("", views.index, name="index"),
    path("perfil/", views.perfil, name="perfil"),
    path("login/", views.login, name="login"),
    path("cadastro/", views.cadastro, name="cadastro")
]