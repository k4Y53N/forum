from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from django.urls import reverse

from . import forms
from .http import HttpResponseUnauthorized

# Create your views here.


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        
        return render(request, 'login.html', {})

    def post(self, request):
        form = forms.UserLoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('invaild form')
        clean_data = form.cleaned_data
        email = clean_data['email']
        password = clean_data['password']
        user = authenticate(email=email, password=password)
        if user == None:
            return HttpResponseUnauthorized()
        login(request, user)
        return redirect('/')


class Logout(View):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        logout(request)
        return redirect('/')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        pass


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
