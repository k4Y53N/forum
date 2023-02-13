from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import RedirectURLMixin
from django.db import IntegrityError

from . import forms
from . import REDIRECT_FIELD_NAME
from .http import HttpResponseUnauthorized, HttpResponseConflict

# Create your views here.


class Login(View, RedirectURLMixin):
    next_page = '/'
    redirect_field_name = REDIRECT_FIELD_NAME

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        context = {
            'next': self.get_success_url(),
            'redirect_field_name': REDIRECT_FIELD_NAME
        }

        return render(request, 'login.html', context)

    def post(self, request):
        form = forms.UserLoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('Enter your email and password!')
        clean_data = form.cleaned_data
        user = authenticate(**clean_data)
        if user == None:
            return HttpResponseUnauthorized('Email or password incorrect!')
        login(request, user)

        return redirect(self.get_success_url())


class Logout(View, RedirectURLMixin):
    next_page = '/'
    redirect_field_name = REDIRECT_FIELD_NAME

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(self.get_success_url())
        context = {
            'next': self.get_success_url(),
            'redirect_field_name': self.redirect_field_name
        }

        return render(request, 'logout.html', context)

    def post(self, request):
        logout(request)
        return redirect(self.get_success_url())


class Register(View):
    def get(self, request):
        context = {
            'form': forms.UserCreateForm()
        }
        return render(request, 'register.html', context)

    def post(self, request):
        form = forms.UserCreateForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('enter correct field or username and email alerady exist')
        clean_data = form.cleaned_data
        username = clean_data['username']
        email = clean_data['email']
        password = clean_data['password']
        try:
            user = get_user_model().objects.create_user(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
        except IntegrityError:
            return HttpResponseConflict('username or email already exist') 
        
        login(request, user)

        return redirect('/')


class PasswordForget(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class PasswordReset(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
