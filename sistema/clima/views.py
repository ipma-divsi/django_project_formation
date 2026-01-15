from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import AvisoMeteorologico, AvisoMar, Comentario, Praia, Noticia
from .forms import ComentarioForm
from datetime import date
from datetime import datetime, timedelta
import requests


def inicio(request):
    return render(request, "publico/inicio.html")

CIDADES = [
    # Açores
    {"nome": "Santa Cruz das Flores", "lat": 39.4558, "lon": -31.1319},
    {"nome": "Horta", "lat": 38.5333, "lon": -28.6333},
    {"nome": "Angra do Heroísmo", "lat": 38.6553, "lon": -27.2173},
    {"nome": "Ponta Delgada", "lat": 37.7412, "lon": -25.6756},

    # Madeira
    {"nome": "Porto Santo", "lat": 33.0707, "lon": -16.3317},
    {"nome": "Funchal", "lat": 32.6669, "lon": -16.9241},

    # Portugal continental
    {"nome": "Viana do Castelo", "lat": 41.6943, "lon": -8.8347},
    {"nome": "Porto", "lat": 41.1496, "lon": -8.611},
    {"nome": "Braga", "lat": 41.5454, "lon": -8.4265},
    {"nome": "Lisboa", "lat": 38.7169, "lon": -9.1397},
    {"nome": "Bragança", "lat": 41.8056, "lon": -6.7575},
    {"nome": "Vila Real", "lat": 41.2956, "lon": -7.7447},
    {"nome": "Aveiro", "lat": 40.6405, "lon": -8.6538},
    {"nome": "Viseu", "lat": 40.661, "lon": -7.9097},
    {"nome": "Guarda", "lat": 40.537, "lon": -7.2658},
    {"nome": "Coimbra", "lat": 40.211, "lon": -8.4297},
    {"nome": "Leiria", "lat": 39.7436, "lon": -8.807},
    {"nome": "Castelo Branco", "lat": 39.8226, "lon": -7.4946},
    {"nome": "Santarém", "lat": 39.2369, "lon": -8.6855},
    {"nome": "Portalegre", "lat": 39.292, "lon": -7.4278},
    {"nome": "Setúbal", "lat": 38.524, "lon": -8.892},
    {"nome": "Évora", "lat": 38.566, "lon": -7.906},
    {"nome": "Sines", "lat": 37.956, "lon": -8.873},
    {"nome": "Beja", "lat": 38.015, "lon": -7.863},
    {"nome": "Sagres", "lat": 37.018, "lon": -8.940},
    {"nome": "Faro", "lat": 37.0194, "lon": -7.9304},
]

def mapa(request):
    cidades_com_tempo = []

    for c in CIDADES:
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Lisbon"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            dados = r.json()

            # Pegando a previsão do primeiro dia
            tmin = dados['daily']['temperature_2m_min'][0]
            tmax = dados['daily']['temperature_2m_max'][0]

            cidades_com_tempo.append({
                "nome": c["nome"],
                "lat": c["lat"],
                "lon": c["lon"],
                "tmin": str(tmin),
                "tmax": str(tmax)
            })
        except Exception as e:
            print(f"Erro {c['nome']}: {e}")
            cidades_com_tempo.append({
                "nome": c["nome"],
                "lat": c["lat"],
                "lon": c["lon"],
                "tmin": "--",
                "tmax": "--"
            })

    avisos = AvisoMeteorologico.objects.all().order_by("-data")

    return render(request, "publico/index.html", {
        "cidades": cidades_com_tempo,
        "avisos": avisos
    })

def detalhe_aviso(request, id):
    aviso = get_object_or_404(AvisoMeteorologico, id=id)
    comentarios = Comentario.objects.filter(aviso=aviso).order_by("-data")

    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.aviso = aviso
            comentario.save()
            return redirect("detalhe_aviso", id=aviso.id)
    else:
        form = ComentarioForm()

    return render(request, "publico/detalhe_aviso.html", {
        "aviso": aviso,
        "comentarios": comentarios,
        "form": form
    })

PRAIAS_BASE = [
    {"nome": "Praia de Carcavelos", "lat": 38.6916, "lon": -9.3380},
    {"nome": "Praia da Rocha", "lat": 37.1183, "lon": -8.5456},
    {"nome": "Praia da Nazaré", "lat": 39.6029, "lon": -9.0701},
    {"nome": "Praia de Matosinhos", "lat": 41.2075, "lon": -8.7203},
]

# =========================
# MAPA DO MAR
# =========================
def mapa_mar(request):
    praias_com_dados = []

    for p in PRAIAS_BASE:
        praias_com_dados.append({
            "nome": p["nome"],
            "lat": p["lat"],
            "lon": p["lon"],
        })

    avisos = AvisoMar.objects.all().order_by("-data")

    return render(request, "publico/mapa_mar.html", {
        "praias": praias_com_dados,
        "avisos": avisos
    })


# =========================
# DETALHE AVISO DO MAR
# (COM comentários)
# =========================
def detalhe_aviso_mar(request, id):
    aviso = get_object_or_404(AvisoMar, id=id)
    
    # Comentários do aviso do mar
    comentarios = Comentario.objects.filter(aviso_mar=aviso).order_by("-data")
    
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.aviso_mar = aviso
            comentario.save()
            return redirect("detalhe_aviso_mar", id=aviso.id)
    else:
        form = ComentarioForm()

    return render(request, "publico/detalhe_aviso_mar.html", {
        "aviso": aviso,
        "comentarios": comentarios,
        "form": form
    })

def noticias(request):
    # Ano vindo da URL (?ano=2026)
    ano = request.GET.get('ano')

    if ano:
        ano = int(ano)
    else:
        ano = date.today().year

    # FILTRO CORRETO
    noticias = Noticia.objects.filter(data__year=ano).order_by('-data')

    # Anos disponíveis para o menu
    anos = Noticia.objects.dates('data', 'year', order='DESC')
    anos = [a.year for a in anos]

    context = {
        'noticias': noticias,
        'ano_atual': ano,
        'anos': anos,
    }

    return render(request, 'publico/noticias.html', context)

def detalhe_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    return render(request, "publico/detalhe_noticia.html", {"noticia": noticia})
# Distritos com cidades — apenas referência para dropdown
DISTRITOS = {
    "Aveiro": ["Águeda", "Albergaria-a-Velha", "Anadia", "Arouca", "Aveiro", "Castelo de Paiva", "Espinho", "Estarreja", "Ílhavo", "Mealhada", "Murtosa", "Oliveira de Azeméis", "Oliveira do Bairro", "Ovar", "Praia da Barra", "Praia da Costa Nova", "Praia da Torreira", "Praia da Vagueira", "Praia de Esmoriz", "Praia de Espinho", "Praia do Jacinto", "Praia de São Pedro da Maceira", "Praia do Furadouro", "Praia do Torrao do Lameiro", "Santa Maria da Feira", "São João da Madeira", "Sever do Vouga", "Vagos", "Vale de Cambra"],
    "Beja": ["Aljustrel", "Almodôvar", "Alvito", "Barrancos", "Beja", "Castro Verde", "Cuba", "Ferreira do Alentejo", "Mértola", "Odemira", "Oura", "Ourique", "Praia de Zambujeira", "Praia de Almograve", "Praia de Milfontes", "Praia do Malhão", "Serpa", "Vidigueira"],
    "Lisboa": ["Alenquer", "Amadora", "Arruda dos Vinhos", "Azambuja", "Cadaval", "Cascais", "Ericeira", "Lisboa", "Lisboa-Ajuda", "Lisboa-Jardim Botanico", "Lisboa-Oriente", "Loures", "Lourinhã", "Mafra", "Odivelas", "Oeiras", "Praia da Adraga", "Praia da Areia Branca", "Praia da Foz do Lizandro", "Praia das Maças", "Praia de Carcavelos", "Praia de Cascais", "Praia de Coxos", "Praia de Ribeira de Ilhas", "Praia de Santa Cruz", "Praia do Guincho", "Praia do Magoito", "Praia Grande", "Sintra", "Sobral de Monte Agraço", "Torres Vedras", "Vila Franca de Xira"],
    # Adicione os demais distritos conforme necessidade
}
# Busca todos os locais válidos do IPMA
def get_cidades_ipma():
    url = "https://api.ipma.pt/open-data/distrits-islands.json"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])
        return {item["local"].strip(): item["globalIdLocal"] for item in data}
    except Exception as e:
        print("Erro ao buscar cidades IPMA:", e)
        return {}

CIDADES_ID = get_cidades_ipma()  # { "Lisboa": 1110600, "Aveiro": 1010500, ... }

# Distritos filtrados apenas pelas cidades que existem no IPMA
def get_distritos_filtrados():
    distritos = {}
    for cidade, id_ in CIDADES_ID.items():
        # extrai distrito do nome da cidade se tiver formato "Lisboa / Lisboa"
        distrito = cidade.split("/")[0].strip()  
        if distrito not in distritos:
            distritos[distrito] = []
        distritos[distrito].append(cidade)
    return distritos

DISTRITOS = get_distritos_filtrados()

def previsao_10_dias(request):
    distrito_selecionado = request.GET.get("distrito")
    cidade_selecionada = request.GET.get("cidade")

    cidades_do_distrito = DISTRITOS.get(distrito_selecionado, []) if distrito_selecionado else []

    previsao = []

    if cidade_selecionada:
        cidade_id = CIDADES_ID.get(cidade_selecionada)
        if cidade_id:
            url = f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{cidade_id}.json"
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                dados = r.json()
                dias = dados.get("data", [])
                for dia in dias[:10]:  # até 10 dias
                    previsao.append({
                        "data": datetime.strptime(dia.get("forecastDate"), "%Y-%m-%d").strftime("%d/%m/%Y"),
                        "tMin": dia.get("tMin"),
                        "tMax": dia.get("tMax"),
                        "precipitaProb": dia.get("precipitaProb"),
                        "estadoCielo": dia.get("idWeatherType"),
                        "ventoDir": dia.get("predWindDir"),
                        "ventoVel": dia.get("classWindSpeed")
                    })
            except Exception as e:
                print(f"Erro ao buscar API IPMA: {e}")

    context = {
        "distritos": DISTRITOS.keys(),
        "distrito_selecionado": distrito_selecionado,
        "cidades_do_distrito": cidades_do_distrito,
        "cidade_selecionada": cidade_selecionada,
        "previsao": previsao,
    }
    return render(request, "publico/previsao_10_dias.html", context)

def previsao_descritiva(request):
    return render(request, "publico/previsao_descritiva.html")

def estacoes_online(request):
    return render(request, "publico/estacoes_online.html")




