from django.shortcuts import render
from .models import Filme
from django.views.generic import TemplateView, ListView, DetailView


# Create your views here.
class Homepage(TemplateView):
    template_name = 'homepage.html'


class Homefilmes(ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # object_list -> lista de itens do modelo (Filme)


class Detalhesfilme(DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object -> 1 item do modelo (Filme)

    def get_context_data(self, **kwargs):
        # preservando as características da função original .get_context_data
        context = super(Detalhesfilme, self).get_context_data(**kwargs)

        # filtrar a minha tabela de filmes pegando os filmes cuja a categoria é igual ao do filme da página (object)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context