from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import FAIXA_ETARIA_CHOICES, NIVEL_CHOICES


class AlterarSenhaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    faixa_etaria = forms.ChoiceField(choices=FAIXA_ETARIA_CHOICES, label='Faixa Etária')
    nivel = forms.ChoiceField(choices=NIVEL_CHOICES, label='Nível')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'faixa_etaria', 'nivel']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.faixa_etaria = self.cleaned_data['faixa_etaria']
            profile.nivel_atual = self.cleaned_data['nivel']
            profile.save()
        return user
