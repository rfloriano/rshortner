from django import forms

from shorter.models import Bit


class BitForm(forms.ModelForm):
    url = forms.URLField(widget=forms.TextInput(attrs={'class': 'span6', 'placeholder': "Digite aqui sua URL"}))

    class Meta:
        model = Bit
        exclude = ['short_url', 'created', 'page_view', 'user']
