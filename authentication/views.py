# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import logout, login
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from forms import LoginForm


class LogoutView(RedirectView):
    pattern_name = 'homepage'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class LoginView(FormView):
    template_name = 'authentication/user_login.html'
    success_url = reverse_lazy('homepage')
    form_class = LoginForm

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['active_page'] = 'login'
        return context

    def form_valid(self, form):
        user = form.login()
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
            else:
                return self.response_error_page('你的账户尚未激活')
        else:
            return self.response_error_page('用户名或密码错误')

    def response_error_page(self, msg):
        return render(self.request, 'utils/error_page.html', {'message': msg})
