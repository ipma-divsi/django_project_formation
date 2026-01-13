from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["nome", "texto"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Seu nome"}),
            "texto": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Escreva seu comentário..."
            }),
        }
