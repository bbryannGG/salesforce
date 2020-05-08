from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.dispatch import receiver

class ProfilePageView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    fields = ( 'username', 'email', 'first_name', 'last_name', 'position', 'contact_number')
    template_name = 'profile.html'
    login_url = 'login'
    success_message = "Account details has been updated successfully"
