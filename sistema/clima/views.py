from django.shortcuts import render, get_object_or_404, redirect
from .models import AvisoMeteorologico, AvisoMar, Comentario, Praia
from .forms import ComentarioForm
import requests


def index(request):
    return render(request, "publico/index.html")


CIDADES = [
    {"id": 1010500, "nome": "Aveiro", "lat": 40.6405, "lon": -8.6538},
    {"id": 1020500, "nome": "Beja", "lat": 38.0151, "lon": -7.8632},
    {"id": 1030300, "nome": "Braga", "lat": 41.5454, "lon": -8.4265},
    {"id": 1040200, "nome": "Bragança", "lat": 41.8061, "lon": -6.7567},
    {"id": 1050200, "nome": "Castelo Branco", "lat": 39.8222, "lon": -7.4909},
    {"id": 1060300, "nome": "Coimbra", "lat": 40.2033, "lon": -8.4103},
    {"id": 1070500, "nome": "Évora", "lat": 38.5714, "lon": -7.9135},
    {"id": 1080500, "nome": "Faro", "lat": 37.0194, "lon": -7.9304},
    {"id": 1090700, "nome": "Guarda", "lat": 40.5373, "lon": -7.2683},
    {"id": 1100900, "nome": "Leiria", "lat": 39.7436, "lon": -8.8071},
    {"id": 1110600, "nome": "Lisboa", "lat": 38.7223, "lon": -9.1393},
    {"id": 1121400, "nome": "Portalegre", "lat": 39.2967, "lon": -7.4285},
    {"id": 1131200, "nome": "Porto", "lat": 41.1579, "lon": -8.6291},
    {"id": 1141600, "nome": "Santarém", "lat": 39.2362, "lon": -8.6859},
    {"id": 1151200, "nome": "Setúbal", "lat": 38.5244, "lon": -8.8882},
    {"id": 1160900, "nome": "Viana do Castelo", "lat": 41.6932, "lon": -8.8329},
    {"id": 1171400, "nome": "Vila Real", "lat": 41.3006, "lon": -7.7441},
    {"id": 1182300, "nome": "Viseu", "lat": 40.6566, "lon": -7.9125},
]

def mapa(request):
    cidades_com_tempo = []

    for c in CIDADES:
        try:
            url = f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{c['id']}.json"
            r = requests.get(url, timeout=5)
            dados = r.json()
            hoje = dados["data"][0]

            cidades_com_tempo.append({
                "nome": c["nome"],
                "lat": c["lat"],
                "lon": c["lon"],
                "tmin": hoje.get("tMin", "--"),
                "tmax": hoje.get("tMax", "--"),
            })
        except:
            cidades_com_tempo.append({
                "nome": c["nome"],
                "lat": c["lat"],
                "lon": c["lon"],
                "tmin": "--",
                "tmax": "--",
            })

    avisos = AvisoMeteorologico.objects.all().order_by("-data")

    return render(request, "publico/tempo.html", {
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


# =========================
# MAPA DO MAR
# =========================
def mapa_mar(request):
    avisos = AvisoMar.objects.all().order_by("-data")
    praias = Praia.objects.all()

    return render(request, "publico/mapa_mar.html", {
        "avisos": avisos,
        "praias": praias
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


def detalhe_praia(request, id):
    praia = get_object_or_404(Praia, id=id)

    return render(request, "publico/detalhe_praia.html", {
        "praia": praia
    })
