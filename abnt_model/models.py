from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20)
    sobrenome = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    senha = models.CharField(max_length=128)
    confirmar_senha = models.CharField(max_length=128)

