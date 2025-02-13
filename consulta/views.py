from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Consulta
from .forms import ConsultaForm
from agendamentos.models import Agendamento
from usuarios.permissions import is_profissional_saude, is_psicologo



# ✅ Criar uma nova consulta (Apenas psicólogos)
@login_required
@user_passes_test(is_psicologo)
@user_passes_test(is_profissional_saude)
def adicionar_consulta(request):
    """Permite que o psicólogo adicione uma nova consulta"""
    
    # Obtém os agendamentos do profissional logado que ainda não foram concluídos
    agendamentos = Agendamento.objects.filter(psicologo=request.user, status="Em andamento")
    
    if not agendamentos.exists():
        messages.error(request, "Nenhum paciente disponível para consulta. Cadastre um agendamento primeiro.")
        return redirect("listar_agendamentos")

    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            
            # Garante que a consulta tenha um paciente
            if not consulta.paciente:
                messages.error(request, "Erro: Selecione um paciente para a consulta.")
                return redirect("adicionar_consulta")

            consulta.profissional = request.user
            consulta.save()
            messages.success(request, "Consulta criada com sucesso!")
            return redirect("listar_consultas")
        else:
            messages.error(request, "Erro ao criar a consulta.")

    else:
        form = ConsultaForm()

    return render(request, "consultas/adicionar_consulta.html", {"form": form, "agendamentos": agendamentos})

# ✅ Listar consultas do profissional logado (Apenas psicólogos)
@login_required
@user_passes_test(is_psicologo)
def listar_consultas(request):
    """Lista todas as consultas do psicólogo logado"""
    consultas = Consulta.objects.filter(profissional=request.user).order_by("-data_consulta")

    return render(request, "consultas/listar_consultas.html", {"consultas": consultas})

# ✅ Realizar consulta (Apenas psicólogos)
@login_required
@user_passes_test(is_psicologo)
def realizar_consulta(request, agendamento_id):
    """Permite que o psicólogo realize uma consulta para um paciente agendado."""
    
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, psicologo=request.user)

    # Cria ou obtém a consulta associada ao agendamento
    consulta, created = Consulta.objects.get_or_create(
        paciente=agendamento.paciente,            
        profissional=request.user,                
        data_consulta=agendamento.data,
        horario_consulta=agendamento.hora,
        defaults={'status': "EM_ANDAMENTO"}
    )

    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit=False)
            
            # Se o botão "concluir" foi pressionado, atualiza o status da consulta e do agendamento
            if "concluir" in request.POST:
                consulta.status = "CONCLUIDO"
                agendamento.status = "Concluído"
                agendamento.save()  
            
            consulta.save()
            messages.success(request, "Consulta concluída com sucesso!")
            return redirect("listar_agendamentos")
        else:
            messages.error(request, "Erro ao atualizar a consulta.")
    
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, "consultas/realizar_consulta.html", {
        "form": form,
        "consulta": consulta,
        "agendamento": agendamento
    })

# ✅ Excluir uma consulta (Apenas psicólogos)
@login_required
@user_passes_test(is_psicologo)
def excluir_consulta(request, consulta_id):
    """Permite que o psicólogo exclua uma consulta"""
    
    consulta = get_object_or_404(Consulta, id=consulta_id, profissional=request.user)
    
    if request.method == "POST":
        consulta.delete()
        messages.success(request, "Consulta excluída com sucesso!")
        return redirect("listar_consultas")

    return render(request, "consultas/confirmar_exclusao.html", {"consulta": consulta})
