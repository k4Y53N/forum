from django import forms


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=15)
