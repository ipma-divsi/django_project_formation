from django.db import models

class AvisoMeteorologico(models.Model):
    NIVEL_CHOICES = [
        ('verde', 'Verde'),
        ('amarelo', 'Amarelo'),
        ('laranja', 'Laranja'),
        ('vermelho', 'Vermelho'),
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    aviso = models.ForeignKey(
        AvisoMeteorologico,
        on_delete=models.CASCADE,
        related_name="comentarios",
        null=True,
        blank=True
    )
    aviso_mar = models.ForeignKey(
        "AvisoMar",  # note as aspas
        on_delete=models.CASCADE,
        related_name="comentarios_mar",
        null=True,
        blank=True
    )
    nome = models.CharField(max_length=50)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.aviso:
            return f"{self.nome} - {self.aviso.titulo}"
        elif self.aviso_mar:
            return f"{self.nome} - {self.aviso_mar.titulo}"
        else:
            return self.nome

class Praia(models.Model):
    nome = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()

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

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateField()
    imagem = models.ImageField(upload_to='noticias/', blank=True, null=True)

    def __str__(self):
        return self.titulo