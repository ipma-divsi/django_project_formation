from django.db import models
from django.contrib.auth.models import User

TIPOS_OBSERVACAO = [
    ('Temp', 'Temperatura'),
    ('Precip', 'Precipitação'),
    ('Vento', 'Vento'),
    ('Ondas', 'Ondas'),
    ('Outro', 'Outro'),
]

class Observacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_OBSERVACAO)
    local = models.CharField(max_length=100)
    valor = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo}) - {self.local}"
