from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from shortener.models import Bit


class BitForm(forms.ModelForm):
    url = forms.URLField(
        widget=forms.TextInput(
            attrs={
                'class': 'span6',
                'placeholder': "Digite aqui sua URL"
            }
        )
    )

    class Meta:
        model = Bit
        exclude = ['short_url', 'created', 'click', 'user']


class AuthForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Username"),
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'span6'
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'span6'
            }
        )
    )
