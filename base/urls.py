from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    DashboardView,
    HomeView,
    SignupView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
]
