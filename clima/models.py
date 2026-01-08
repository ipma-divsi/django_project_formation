from django.db import models

class AvisoMeteorologico(models.Model):
    NIVEL_CHOICES = [
        ('verde', 'Verde'),
        ('amarelo', 'Amarelo'),
        ('laranja', 'Laranja'),
        ('vermelho', 'Vermelho'),
    ]

    TIPO_CHOICES = [
        ('tempo', 'Tempo'),
        ('mar', 'Mar'),
        ('ambos', 'Tempo e Mar'),
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    aviso = models.ForeignKey(
        AvisoMeteorologico,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    nome = models.CharField(max_length=50)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.aviso.titulo}"


class Praia(models.Model):
    nome = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    altura_onda = models.FloatField(null=True, blank=True)
    direcao_onda = models.CharField(max_length=50, blank=True)
    temp_agua = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nome


class AvisoMar(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    nivel = models.CharField(
        max_length=20,
        choices=[
            ('verde', 'Verde'),
            ('amarelo', 'Amarelo'),
            ('laranja', 'Laranja'),
            ('vermelho', 'Vermelho'),
        ]
    )
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
 