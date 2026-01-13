from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

# Para observações
TIPOS_OBSERVACAO = [
    ('Temp', 'Temperatura'),
    ('Precip', 'Precipitação'),
    ('Vento', 'Vento'),
    ('Ondas', 'Ondas'),
    ('Sismos', 'Sismos'),
    ('Outro', 'Outro'),
]

class Observacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_OBSERVACAO)
    local = models.CharField(max_length=100)
    valor = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo}) - {self.local}"

    def save(self, *args, **kwargs):
        # Se não existir latitude/longitude mas houver local, tenta geocodificar via Nominatim
        if (self.latitude is None or self.longitude is None) and self.local:
            try:
                session = requests.Session()
                session.headers.update({'User-Agent': 'django_project_formation_map/1.0 (contact@example.com)'})
                query = f"{self.local}, Portugal"
                resp = session.get('https://nominatim.openstreetmap.org/search', params={'q': query, 'format': 'json', 'limit': 1}, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    if data:
                        item = data[0]
                        # Verifica se o resultado corresponde a Portugal
                        display = item.get('display_name', '')
                        if 'Portugal' in display:
                            try:
                                self.latitude = float(item.get('lat'))
                                self.longitude = float(item.get('lon'))
                            except Exception:
                                pass
            except Exception:
                # Em caso de erro de rede ou limites, apenas continua sem coordenadas
                pass

            # Fallback para cidades/regiões de Portugal quando o Nominatim não responde
            if (self.latitude is None or self.longitude is None) and self.local:
                local_l = self.local.strip().lower()
                FALLBACK = {
                    # Principais cidades (Distritos)
                    'porto': (41.1579, -8.6291),
                    'lisboa': (38.7223, -9.1393),
                    'faro': (37.0194, -7.9308),
                    'coimbra': (40.2033, -8.4103),
                    'braga': (41.5454, -8.4265),
                    'aveiro': (40.6405, -8.6538),
                    'viseu': (40.6619, -7.2645),
                    'guarda': (40.5365, -6.7664),
                    'bragança': (41.8056, -6.7570),
                    'viana do castelo': (41.6933, -8.8343),
                    'vila real': (41.2903, -7.7469),
                    'évora': (38.6647, -7.9064),
                    'castelo branco': (40.2837, -6.4925),
                    'portalegre': (39.2943, -7.4261),
                    'santarém': (39.2331, -8.7285),
                    'leiria': (39.7453, -8.7578),
                    'setúbal': (38.5245, -8.8881),
                    # Cidades grandes/importantes
                    'almada': (38.6797, -9.1601),
                    'oeiras': (38.6706, -9.3133),
                    'queluz': (38.7544, -9.2544),
                    'barreiro': (38.6651, -9.0733),
                    'seixal': (38.6390, -9.1013),
                    'loures': (38.8234, -9.1636),
                    'sintra': (38.7767, -9.3911),
                    'cascais': (38.6876, -9.4205),
                    'estoril': (38.7137, -9.4073),
                    'odivelas': (38.7898, -9.1568),
                    'amadora': (38.7535, -9.2356),
                    'brás de cruz': (38.7667, -9.2333),
                    'mafra': (38.9362, -9.3158),
                    'torres vedras': (39.0833, -9.2667),
                    'caldas da rainha': (39.3667, -9.1333),
                    'óbidos': (39.3603, -9.1639),
                    'peniche': (39.3582, -9.3618),
                    'ericeira': (38.9633, -9.4187),
                    'nazaré': (39.6012, -9.0653),
                    'alcobaça': (39.5533, -8.9733),
                    'batalha': (39.6645, -8.7650),
                    'fátima': (39.6286, -8.6533),
                    'castelo de paiva': (40.9167, -8.5000),
                    'arouca': (40.9333, -8.2500),
                    'santa maria da feira': (40.9167, -8.5333),
                    'oliveira de azeméis': (40.8000, -8.4667),
                    'vila nova de gaia': (41.1333, -8.6167),
                    'vila do conde': (41.3407, -8.7518),
                    'póvoa de varzim': (41.3833, -8.7667),
                    'espinho': (40.6333, -8.6333),
                    'ovar': (40.8708, -8.7708),
                    'sever do vouga': (40.7667, -8.4000),
                    'mortágua': (40.6167, -8.3000),
                    'cantanhede': (40.3233, -8.2633),
                    'mealhada': (40.3667, -8.3500),
                    'anadia': (40.5067, -8.4333),
                    'oliveira do hospital': (40.4667, -7.8500),
                    'penalva do castelo': (40.5667, -7.5500),
                    'nelas': (40.6167, -7.6167),
                    'aguarda': (40.6500, -7.7667),
                    'sítio da nazaré': (39.6012, -9.0653),
                    'caldas de monchique': (37.3167, -8.5833),
                    'lagoa': (37.1414, -8.9261),
                    'silves': (37.1903, -8.4416),
                    'carmo': (37.3844, -8.2388),
                    'albufeira': (37.0899, -8.2506),
                    'vilamoura': (37.0704, -8.1226),
                    'olhão': (37.0263, -7.8418),
                    'tavira': (37.1414, -7.8914),
                    'quarteira': (37.0635, -8.0958),
                    'loulé': (37.1414, -8.0258),
                    'são brás de alportel': (37.1703, -7.8918),
                    'estômbar': (37.2833, -8.5167),
                    'monchique': (37.3167, -8.5667),
                    # Regiões e zonas turísticas
                    'algarve': (37.1622, -7.9498),
                    'alentejo': (38.3368, -8.0020),
                    'ribatejo': (39.3000, -8.5000),
                    'beira interior': (40.3000, -6.8000),
                    'beira baixa': (40.2000, -6.7000),
                    'dão': (40.4500, -8.0000),
                    'mondego': (40.1000, -8.4000),
                    'minho': (41.6500, -8.6500),
                    'douro litoral': (41.1500, -8.5000),
                    'douro': (41.1533, -7.2769),
                    'tejo': (38.6500, -8.8500),
                    'vouga': (40.8000, -8.5000),
                    'mira': (40.3500, -8.8000),
                    # Serras e paisagem
                    'serra da estrela': (40.3328, -7.5975),
                    'peneda gerês': (41.7422, -8.1628),
                    'serra monchique': (37.3167, -8.5667),
                    'serra da arrábida': (38.4833, -9.0167),
                    'serra sintra': (38.7833, -9.3667),
                    'serra aires': (39.7667, -8.2333),
                    'serra candeeiros': (39.6333, -8.7667),
                    'pico da serra da estrela': (40.3328, -7.5975),
                    # Ilhas
                    'madeira': (32.7607, -16.9595),
                    'funchal': (32.6669, -16.9241),
                    'câmara de lobos': (32.6333, -16.9667),
                    'ponta delgada': (37.7412, -25.6756),
                    'são miguel': (37.7412, -25.6756),
                    'açores': (37.7412, -25.6756),
                    'terceira': (38.6597, -27.0633),
                    'faial': (38.5332, -28.7183),
                    'são jorge': (38.6597, -28.0806),
                    'graciosa': (39.0333, -27.9833),
                    'santa maria': (37.0167, -25.1333),
                    'são bartolomeu': (36.9500, -25.0833),
                    # Outros locais importantes
                    'torres vedras': (39.0833, -9.2667),
                    'serra branca': (40.2500, -7.1500),
                    'covilhã': (40.2833, -7.5000),
                    'fundão': (40.1333, -7.5000),
                    'penamacor': (40.2167, -7.1667),
                    'idanha-a-velha': (40.0667, -7.0833),
                    'sabugal': (40.3833, -7.1167),
                    'manteigas': (40.3833, -7.5000),
                    'gouveia': (40.4833, -7.5500),
                    'seia': (40.6833, -7.7000),
                    'fornos de algodres': (40.5500, -7.5667),
                    'trancoso': (40.7667, -7.1500),
                    'mêda': (40.7833, -7.2167),
                    'pinhel': (40.7500, -7.0833),
                    'sortelha': (40.5000, -7.0833),
                    'almeida': (40.7167, -6.9333),
                    'celorico da beira': (40.7167, -7.5000),
                    'vila nova de foz côa': (40.7500, -7.1333),
                }
                for k, (lat, lon) in FALLBACK.items():
                    if k in local_l:
                        self.latitude = lat
                        self.longitude = lon
                        break

        super().save(*args, **kwargs)


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
