from django.db import models
from django.contrib.auth.models import User

class Image(models.Model): #associação com a classe User.
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='image')
    image = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.user.username  # or self.user.email, or another string attribute of User

class Documentos_Abstract(models.Model): #classe Abstrata, como modelo padrão
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_do_arquivo= models.TextField(unique=True)
    autor = models.TextField()
    titulo = models.TextField()
    introducao= models.TextField()
    desenvolvimento = models.TextField()
    conclusao = models.TextField()
    class Meta:
        abstract=True

class Ensaio(Documentos_Abstract): #classe que herda da abstrata
    url_imagem = models.URLField() 
    instituicao = models.TextField()
    local = models.TextField()
    ano = models.TextField()
    resumo = models.TextField()
    palavras_chaves = models.TextField()
    abstract = models.TextField()
    keywords = models.TextField()
    problematizacao = models.TextField()
    justificativa = models.TextField()
    questao_geral = models.TextField()
    objetivo = models.TextField()
    metodologia = models.TextField()
    analise_discussao = models.TextField()
    referencias = models.TextField()



    # [...]

#models é um arquivo que modela dados.
