from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Observacao, Profile
from .forms import ObservacaoForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm

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
            return redirect('dashboard')
        else:
            messages.error(request, "Username ou password incorretos")

    return render(request, 'core/login.html')

# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):
    logout(request)
    return redirect('home')

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

        # Criar usuário
        user = User.objects.create_user(username=username, email=email, password=password1)
        # Criar perfil vazio para o usuário
        Profile.objects.create(user=user)
        messages.success(request, "Conta criada com sucesso! Já podes fazer login.")
        return redirect('login')

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
            return redirect('dashboard')  # redireciona para atualizar a lista
    else:
        form = ObservacaoForm()

    # Buscar todas as observações do usuário para mostrar no dashboard
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
    """Lista e permite adicionar observações do usuário."""
    observacoes = Observacao.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ObservacaoForm(request.POST)
        if form.is_valid():
            nova_obs = form.save(commit=False)
            nova_obs.user = request.user
            nova_obs.save()
            messages.success(request, "Observação adicionada com sucesso!")
            return redirect('minhas_observacoes')
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
            return redirect('minhas_observacoes')
    else:
        form = ObservacaoForm(instance=obs)

    return render(request, 'core/editar_observacao.html', {'form': form, 'observacao': obs})

@login_required
def deletar_observacao(request, pk):
    obs = get_object_or_404(Observacao, pk=pk, user=request.user)
    if request.method == 'POST':
        obs.delete()
        messages.success(request, "Observação deletada com sucesso!")
        return redirect('minhas_observacoes')

    return render(request, 'core/deletar_observacao.html', {'observacao': obs})

# -------------------------
# FEED GLOBAL
# -------------------------
@login_required
def feed(request):
    """Feed global estilo Twitter: mostra todas as observações de todos os usuários."""
    observacoes = Observacao.objects.all().order_by('-created_at')
    return render(request, 'core/feed.html', {'observacoes': observacoes})

# -------------------------
# PERFIL
# -------------------------
@login_required
def perfil(request):
    """Perfil interativo: editar dados, foto, bio, data de nascimento e senha."""
    # Inicializar formulários com dados atuais do usuário
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        # Verificar qual formulário foi enviado
        if 'update_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Perfil atualizado com sucesso!")
                return redirect('perfil')

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Mantém o usuário logado
                messages.success(request, "Senha alterada com sucesso!")
                return redirect('perfil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = CustomPasswordChangeForm(user=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'core/perfil.html', context)

@login_required
def minhas_observacoes(request):
    observacoes = Observacao.objects.filter(user=request.user).order_by('-created_at')
    form = ObservacaoForm()
    return render(request, 'core/minhas_observacoes.html', {'observacoes': observacoes, 'form': form})
