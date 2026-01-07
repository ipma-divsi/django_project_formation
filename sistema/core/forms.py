from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Observacao, Profile

# Formulário de Observação (já tens)
class ObservacaoForm(forms.ModelForm):
    class Meta:
        model = Observacao
        fields = ['titulo', 'tipo', 'local', 'valor']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título da Observação'}),
            'tipo': forms.Select(),
            'local': forms.TextInput(attrs={'placeholder': 'Local (ex: Porto)'}),
            'valor': forms.TextInput(attrs={'placeholder': 'Valor / Descrição'}),
        }

# Formulário para atualizar User (username e email)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# Formulário para atualizar Profile (foto, bio, data de nascimento)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto', 'bio', 'data_nascimento']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva algo sobre você...'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

# Formulário para alterar senha (opcional)
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha atual'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repita a nova senha'}))
