from django.contrib import admin
from .models import Image, Simple_TCC
class ListImage(admin.ModelAdmin):
    list_display = ("user",)
    list_per_page = 10

admin.site.register(Image,ListImage)

class ListDocumentsForUser(admin.ModelAdmin):
    list_display = ("user",)
    list_per_page = 10

admin.site.register(Simple_TCC,ListImage)