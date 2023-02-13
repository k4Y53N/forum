from django import forms
from django.contrib.auth import get_user_model

class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=20)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']



# class UserCreateForm(forms.Form):
#     username = forms.CharField(max_length=10)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=15)