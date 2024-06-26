from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHomepage
from django.http import HttpResponseRedirect


# Create your views here.
class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('app_filme:homefilmes') # redireciona para homefilmes
        else:
            return super().get(request, *args, **kwargs) #redireciona para a homepage

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('app_filme:login')
        else:
            return reverse('app_filme:criarconta')


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # object_list -> lista de itens do modelo (Filme)


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object -> 1 item do modelo (Filme)

    def get(self, request, *args, **kwargs):
        # contabilizando uma visualização
        filme = self.get_object() # descobrir qual filme está acessando
        filme.visualizações += 1 # somar 1 nas visualizações daquele filme
        filme.save()

        # adicionando o objeto 'filme' no campo 'filmes_vistos' do usuário logado
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) # redireciona user para url desejada

    def get_context_data(self, **kwargs):
        # preservando as características da função original .get_context_data
        context = super(Detalhesfilme, self).get_context_data(**kwargs)

        # filtrar a minha tabela de filmes pegando os filmes cuja a categoria é igual ao do filme da página (object)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context


class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Filme

    # editando object_list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class PaginaPerfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.id != self.kwargs['pk']:
                return self.redirecionar_proprio_perfil()
        else:
            return HttpResponseRedirect(reverse('app_filme:login'))
        return super().dispatch(request, *args, **kwargs)

    def redirecionar_proprio_perfil(self):
        proprio_perfil_url = reverse('app_filme:editarperfil', kwargs={'pk': self.request.user.id})
        return HttpResponseRedirect(proprio_perfil_url)

    def get_success_url(self):
        return reverse('app_filme:homefilmes')


class CriarConta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('app_filme:login')