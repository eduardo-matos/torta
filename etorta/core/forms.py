# coding: utf-8

from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        self.user = authenticate(username=username, password=password)

        if not self.user:
            raise forms.ValidationError('Usuário não encontrado')

        return cleaned_data
