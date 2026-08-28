from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AlterarSenhaForm, RegistroForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'users/login.html')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'users/registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def alterar_senha_view(request):
    if request.method == 'POST':
        form = AlterarSenhaForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('dashboard')
    else:
        form = AlterarSenhaForm(request.user)
    return render(request, 'users/alterar_senha.html', {'form': form})
