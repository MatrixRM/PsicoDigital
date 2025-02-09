from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente
from .forms import PacienteForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test




# ✅ Função para verificar se o usuário pode acessar a listagem de clientes
def pode_acessar_pacientes(user):
    return user.tipo_usuario in ["SECRETARIA", "PROFISSIONAL_SAUDE"]

@login_required
@user_passes_test(pode_acessar_pacientes)
def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by("nome")  # ✅ Ordenação alfabética
    return render(request, "pacientes/listar_pacientes.html", {"pacientes": pacientes})






# ✅ View para cadastrar um novo paciente
@user_passes_test(pode_acessar_pacientes)
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente cadastrado com sucesso!")
            return redirect('listar_pacientes')  # Redireciona para a listagem de pacientes
        else:
            messages.error(request, "Erro no cadastro. Verifique os campos e tente novamente.")
    else:
        form = PacienteForm()
    
    return render(request, 'pacientes/cadastrar_paciente.html', {'form': form})

@user_passes_test(pode_acessar_pacientes)
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente atualizado com sucesso!")
            return redirect('listar_pacientes')  # Redireciona para a listagem
    else:
        form = PacienteForm(instance=paciente)
    
    return render(request, 'pacientes/editar_paciente.html', {'form': form, 'paciente': paciente})






@login_required
@user_passes_test(pode_acessar_pacientes)
def excluir_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == "POST":
        paciente.delete()
        return JsonResponse({"success": True})  # Retorna JSON confirmando exclusão
    
    return JsonResponse({"success": False, "error": "Método inválido"})

