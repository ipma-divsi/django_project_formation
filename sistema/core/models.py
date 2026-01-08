from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Para observações
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


# Modelo para perfil avançado do usuário
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    bio = models.TextField(blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


# -------------------------
# SIGNALS: cria e salva Profile automaticamente
# -------------------------
@receiver(post_save, sender=User)
def criar_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_profile(sender, instance, **kwargs):
    instance.profile.save()
