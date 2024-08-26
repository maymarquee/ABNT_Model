
# aqui é onde registramos as tabelas do banco de dados para que apareça na pagina admin do django.

from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nome', 'sobrenome', 'email')
    search_fields = ('nome', 'email')

