from django.contrib import admin
from .models import Image
class ListImage(admin.ModelAdmin):
    list_display = ("user",)
    list_per_page = 10

admin.site.register(Image,ListImage)