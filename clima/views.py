from django.shortcuts import render, get_object_or_404, redirect
from .models import AvisoMeteorologico, AvisoMar, Comentario, Praia
from .forms import ComentarioForm
import requests

def inicio(request):
    return render(request, "publico/inicio.html")

CIDADES = [
    # ... tua lista de cidades ...
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

def mapa_mar(request):
    # Pega todos os avisos marítimos, ordenados pela data mais recente
    avisos = AvisoMar.objects.all().order_by('-data')
    praias = Praia.objects.all()
    
    return render(request, "publico/mapa.html", {
        "praias": praias,
        "avisos": avisos
    })


def detalhe_praia(request, id):
    praia = get_object_or_404(Praia, id=id)
    avisos = praia.avisos.all().order_by("-data")
    return render(request, "publico/detalhe_praia.html", {
        "praia": praia,
        "avisos": avisos
    })

def mar(request):
    avisos_mar = AvisoMeteorologico.objects.filter(tipo__in=['mar', 'ambos']).order_by('-data')

    return render(request, "publico/mar.html", {
        "avisos_mar": avisos_mar
    })
def detalhe_aviso_mar(request, id):
    aviso = get_object_or_404(AvisoMar, id=id)
    comentarios = Comentario.objects.filter(aviso_mar=aviso).order_by("-criado_em")

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
