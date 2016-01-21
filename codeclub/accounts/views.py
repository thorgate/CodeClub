from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import login as django_login
from django.shortcuts import redirect
from django.views.generic import TemplateView

from accounts.forms import LoginForm, ProfileForm, RegisterForm
from accounts.mixins import ProtectedMixin


def login(request):
    response = django_login(request, template_name='accounts/login.html', authentication_form=LoginForm)

    return response


class RegisterView(TemplateView):
    template_name = "accounts/register.html"

    def get(self, request, *args, **kwargs):

        form = RegisterForm(request.POST or None)

        if form.is_valid():
            form.save()

            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')

        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class SettingsView(ProtectedMixin, TemplateView):
    template_name = "accounts/settings.html"

    def get(self, request, *args, **kwargs):

        form = ProfileForm(request.POST or None, instance=self.request.user)

        if form.is_valid():
            form.save()

            return redirect('dashboard')

        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
