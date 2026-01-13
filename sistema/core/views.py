from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Observacao, Profile
from .forms import ObservacaoForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
import requests
import json

# -------------------------
# PÁGINA INICIAL
# -------------------------
def home(request):
    return render(request, 'core/home.html')


# -------------------------
# LOGIN
# -------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Username ou password incorretos")

    return render(request, 'core/login.html')


def view_clima(request):
    return render(request,'clima/inicio.html')

# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):
    logout(request)
    return redirect('core:home')


# -------------------------
# REGISTRO DE NOVOS USUÁRIOS
# -------------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Verificações básicas
        if password1 != password2:
            messages.error(request, "As passwords não coincidem")
            return render(request, 'core/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este utilizador já existe")
            return render(request, 'core/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está em uso")
            return render(request, 'core/register.html')

        # Criar usuário (o signal em models.py já cria o Profile automaticamente)
        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Conta criada com sucesso! Já podes fazer login.")
        return redirect('core:login')

    return render(request, 'core/register.html')


# -------------------------
# DASHBOARD
# -------------------------
@login_required
def dashboard(request):
    """Dashboard com informações do usuário, CRUD de observações e outros cards."""

    # Processar form de adicionar observação
    if request.method == 'POST':
        form = ObservacaoForm(request.POST)
        if form.is_valid():
            nova_obs = form.save(commit=False)
            nova_obs.user = request.user
            nova_obs.save()
            messages.success(request, "Observação adicionada com sucesso!")
            return redirect('dashboard')
    else:
        form = ObservacaoForm()

    observacoes = Observacao.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'core/dashboard.html', {
        'form': form,
        'observacoes': observacoes
    })


# -------------------------
# MINHAS OBSERVAÇÕES (CRUD)
# -------------------------
@login_required
def minhas_observacoes(request):
    observacoes = Observacao.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ObservacaoForm(request.POST)
        if form.is_valid():
            nova_obs = form.save(commit=False)
            nova_obs.user = request.user
            nova_obs.save()
            messages.success(request, "Observação adicionada com sucesso!")
            return redirect('core:minhas_observacoes')
    else:
        form = ObservacaoForm()

    return render(request, 'core/minhas_observacoes.html', {
        'observacoes': observacoes,
        'form': form
    })


@login_required
def editar_observacao(request, pk):
    obs = get_object_or_404(Observacao, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ObservacaoForm(request.POST, instance=obs)
        if form.is_valid():
            form.save()
            messages.success(request, "Observação atualizada com sucesso!")
            return redirect('core:minhas_observacoes')
    else:
        form = ObservacaoForm(instance=obs)

    return render(request, 'core/editar_observacao.html', {'form': form, 'observacao': obs})


@login_required
def deletar_observacao(request, pk):
    obs = get_object_or_404(Observacao, pk=pk, user=request.user)
    if request.method == 'POST':
        obs.delete()
        messages.success(request, "Observação deletada com sucesso!")
        return redirect('core:minhas_observacoes')

    return render(request, 'core/deletar_observacao.html', {'observacao': obs})


# -------------------------
# FEED GLOBAL
# -------------------------
@login_required
def feed(request):
    observacoes = Observacao.objects.all().order_by('-created_at')
    return render(request, 'core/feed.html', {'observacoes': observacoes})


# -------------------------
# PERFIL
# -------------------------
@login_required
def perfil(request):
    """Perfil interativo: editar dados, foto, bio, data de nascimento, senha e observações."""

    # Inicializar formulários
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    password_form = CustomPasswordChangeForm(user=request.user)
    obs_form = ObservacaoForm()

    # Buscar observações do usuário
    observacoes = Observacao.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        # Atualizar perfil
        if 'update_profile' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Perfil atualizado com sucesso!")
                return redirect('core:perfil')

        # Alterar senha
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Senha alterada com sucesso!")
                return redirect('core:perfil')

        # Adicionar observação
        elif 'add_obs' in request.POST:
            obs_form = ObservacaoForm(request.POST)
            if obs_form.is_valid():
                nova_obs = obs_form.save(commit=False)
                nova_obs.user = request.user
                nova_obs.save()
                messages.success(request, "Observação adicionada com sucesso!")
                return redirect('perfil')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'obs_form': obs_form,
        'observacoes': observacoes,
    }

    return render(request, 'core/perfil.html', context)


def mapa(request):
    """Página com mapa das observações. Opcional: filtrar por usuário via ?user=username"""
    user_filter = request.GET.get('user')
    if user_filter:
        observacoes = Observacao.objects.filter(user__username=user_filter, latitude__isnull=False, longitude__isnull=False).select_related('user').order_by('-created_at')
    else:
        observacoes = Observacao.objects.filter(latitude__isnull=False, longitude__isnull=False).select_related('user').order_by('-created_at')

    markers = []

    for obs in observacoes:
        # Usar coordenadas armazenadas (sem geocoding na view)
        lat = obs.latitude
        lon = obs.longitude

        if lat is None or lon is None:
            continue

        # Extrair intensidade numérica com valores reais (sem normalizar)
        intensity = None
        try:
            import re
            v = str(obs.valor).strip()
            v = v.replace(',', '.')
            # Extrai primeiro número encontrado
            m = re.search(r"(\d+(?:\.\d+)?)", v)
            if m:
                intensity = float(m.group(1))
        except Exception:
            intensity = None

        # Determinar unidade por tipo
        unidade = ''
        if obs.tipo == 'Temp':
            unidade = '°C'
        elif obs.tipo == 'Precip':
            unidade = 'mm'
        elif obs.tipo == 'Vento':
            unidade = 'km/h'
        elif obs.tipo == 'Ondas':
            unidade = 'm'
        elif obs.tipo == 'Sismos':
            unidade = 'magnitude'

        markers.append({
            'lat': float(lat),
            'lng': float(lon),
            'titulo': obs.titulo,
            'user': obs.user.username,
            'tipo': obs.tipo,
            'tipo_display': obs.get_tipo_display(),
            'local': obs.local,
            'valor': obs.valor,
            'unidade': unidade,
            'created_at': obs.created_at.isoformat(),
            'intensity': intensity,
        })

    markers_json = json.dumps(markers)
    return render(request, 'core/mapa.html', {'markers_json': markers_json})
