from django.shortcuts import render, redirect
from django.views.generic import FormView
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from QRinventory import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template.loader import get_template
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from QRinventory import settings
from django.urls import reverse

def register(request):
    return render(request, 'registration/register.html')

def register_new_user(form, request):
    existing_user = User.objects.filter(email=form.cleaned_data['email'])

    if existing_user.exists():
        password_reset_url = request.scheme + '://' + request.get_host() + reverse('password_reset')
        raise IntegrityError("Email already exists: %s" % form.cleaned_data['email'])
    else:
        # Create and log in user
        newly_created_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'])
        login(request, newly_created_user)

class RegisterForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_password_confirm(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise ValidationError('Password fields do not match')
        

class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        try:
            register_new_user(form, self.request)
            messages.success(self.request, 'Thank you for registering. Please login your new Account!')
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        except IntegrityError as e:
            return redirect('/register')
