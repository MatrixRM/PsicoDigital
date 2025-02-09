from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UsuarioForm


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Redireciona para a página inicial
        else:
            messages.error(request, "Usuário ou senha inválidos.")  # Mensagem de erro

    return render(request, "usuarios/login.html")


# ✅ View para logout
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect("login")



def is_admin(user):
    return user.is_authenticated and user.tipo_usuario == "ADMIN"

@login_required
@user_passes_test(is_admin)
def registrar_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Ajustado para password1
            user.save()
            return redirect("login")  # Redirecionar após o cadastro
    else:
        form = UsuarioForm()
    return render(request, "usuarios/registrar.html", {"form": form})


