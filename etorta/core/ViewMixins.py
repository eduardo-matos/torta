from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class TipoContextDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TipoContextDataMixin, self).get_context_data(**kwargs)
        context['tipo'] = self.kwargs['tipo']
        return context
