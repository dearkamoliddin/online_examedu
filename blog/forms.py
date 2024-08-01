from django import forms
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=128)
    password2 = forms.CharField(max_length=128)

    class Meta:
        model = UserModel
        fields = ['username', 'email',]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
