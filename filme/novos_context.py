from .models import Filme


def lista_filmes_recente(request):
    # ordenando em ordem decrescente
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8]
    return {"lista_filmes_recentes": lista_filmes}


def lista_filmes_emAlta(request):
    # ordenando em ordem decrescente
    lista_filmes = Filme.objects.all().order_by('-visualizações')[0:8]
    return {"lista_filmes_emAlta": lista_filmes}


def filme_destaque(request):
    filme = Filme.objects.order_by('-data_criacao').first()
    return {"filme_destaque": filme}