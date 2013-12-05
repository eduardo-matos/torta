from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from .models import Produto, Loja, Url
from api.forms import ProdutoForm
from django.core.urlresolvers import reverse_lazy as r
from api.views import get_model_e_form_por_tipo
from .forms import LoginForm
from etorta.settings.base import LOGIN_REDIRECT_URL
from django.contrib.auth import login, logout as logout_user
from .ViewMixins import LoginRequiredMixin, TipoContextDataMixin


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = r('core:home')

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(*args, **kwargs)

        next = self.request.GET.get('next', None)
        if next:
            context['next'] = next

        return context

    def form_valid(self, form):
        login(self.request, form.user)

        next = self.request.POST.get('next', None)
        url_redirect = next if next else LOGIN_REDIRECT_URL

        return HttpResponseRedirect(url_redirect)


def logout(request):
    logout_user(request)

    from django.core.urlresolvers import reverse
    return HttpResponseRedirect(reverse('core:home'))


class HomeView(TemplateView):
    template_name = 'core/home.html'


class ProdutosView(LoginRequiredMixin, ListView):
    template_name = 'core/produtos.html'
    model = Produto
    context_object_name = 'produtos'


class ModelCriarView(LoginRequiredMixin, TipoContextDataMixin, CreateView):
    template_name = 'core/model-criar.html'
    success_url = r('core:produtos')

    def form_valid(self, form):
        model_instance = form.save(commit=False)

        if isinstance(model_instance, Loja):
            model_instance.dono = self.request.user

        return super(ModelCriarView, self).form_valid(form)

    def get_form_class(self):
        form_class, _ = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return form_class


class ModelAtualizarView(LoginRequiredMixin, TipoContextDataMixin, UpdateView):
    template_name = 'core/model-atualizar.html'
    success_url = r('core:produtos')

    def form_valid(self, form):
        form.save()
        return super(ModelAtualizarView, self).form_valid(form)

    def get_queryset(self):
        _, model_class = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return model_class.objects.all()

    def get_form_class(self):
        form_class, _ = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return form_class


class ModelRemoverView(LoginRequiredMixin, TipoContextDataMixin, DeleteView):
    template_name = 'core/model-remover.html'
    success_url = r('core:produtos')

    def get_model(self):
        _, model_class = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return model_class

    def get_queryset(self):
        _, model_class = get_model_e_form_por_tipo(self.kwargs['tipo'])
        return model_class.objects.all()
