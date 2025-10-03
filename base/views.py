from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import UserRegistrationForm


class HomeView(TemplateView):
    template_name = "base/home.html"


class SignupView(CreateView):
    form_class = UserRegistrationForm
    template_name = "base/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return redirect("dashboard")


class CustomLoginView(LoginView):
    template_name = "base/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("dashboard")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {css}".strip()
        return form


class CustomLogoutView(LogoutView):
    template_name = "base/logged_out.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "base/dashboard.html"
