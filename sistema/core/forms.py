from django import forms
from .models import Observacao

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
