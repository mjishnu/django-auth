from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    DashboardView,
    HomeView,
    SignupView,
    blog_detail,
    blog_list,
    create_blog,
    edit_blog,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("blogs/new/", create_blog, name="create_blog"),
    path("blogs/<int:pk>/edit/", edit_blog, name="edit_blog"),
    path("blogs/<int:pk>/", blog_detail, name="blog_detail"),
    path("blogs/", blog_list, name="blog_list"),
]
