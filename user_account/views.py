from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "user_account/register.html"
    success_url = reverse_lazy("user_account:login")


class CustomLoginView(LoginView):
    template_name = "user_account/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("user_account:login")


class ProfileView(TemplateView):
    template_name = "user_account/profile.html"
