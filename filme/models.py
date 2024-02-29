from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

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
class Episodio(models.Model):
    filme = models.ForeignKey('Filme', related_name='episodios', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + ' - ' + self.titulo


# Criar o usuário
class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")