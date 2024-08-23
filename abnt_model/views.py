from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'abnt_model/index.html')

def perfil(request):
    return render(request, 'abnt_model/perfil.html')

def login(request):
    return render(request, 'abnt_model/login.html')

def cadastro(request):
    return render(request, 'abnt_model/cadastro.html')