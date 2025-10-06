from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import BlogPostForm, UserRegistrationForm
from .models import BlogPost, Category, User


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_type == User.UserTypes.DOCTOR:
            context["posts"] = (
                BlogPost.objects.filter(author=self.request.user)
                .select_related("category")
                .order_by("-created_at")
            )
        return context


@login_required
def create_blog(request):
    if request.user.user_type != User.UserTypes.DOCTOR:
        raise PermissionDenied("Only doctors can create blog posts.")
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = BlogPostForm(user=request.user)
    return render(request, "base/create_blog.html", {"form": form})


def blog_list(request):
    public_posts_qs = (
        BlogPost.objects.filter(is_draft=False)
        .select_related("author", "category")
        .order_by("-created_at")
    )
    categories = Category.objects.all().prefetch_related(
        Prefetch("blog_posts", queryset=public_posts_qs, to_attr="public_posts")
    )
    return render(request, "base/blog_list.html", {"categories": categories})
