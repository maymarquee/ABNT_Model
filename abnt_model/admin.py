from django.contrib import admin
from .models import Image, Ensaio
class ListImage(admin.ModelAdmin):
    list_display = ("user",) #
    list_per_page = 10 #qtd de objetos por pagina


class ListDocumentsForUser(admin.ModelAdmin):
    list_display = ("nome_do_arquivo","user", )
    list_filter= ("user",)
    list_per_page = 10

admin.site.register(Image,ListImage)
admin.site.register(Ensaio,ListDocumentsForUser)