from django.db import models
from django.utils import timezone

# Create your models here.

# Criar o filme
LISTA_CATEGORIAS = (
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros"),
)

class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=10000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    visualizações = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

# Criar o episódio

# Criar o usuário