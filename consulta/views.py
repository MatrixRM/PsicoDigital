from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Consulta
from .forms import ConsultaForm
from agendamentos.models import Agendamento

# ✅ Todos os profissionais de saúde podem ver agendamentos
def is_profissional_saude(user):
    return user.is_authenticated and user.tipo_usuario in ["PROFISSIONAL_SAUDE", "PSICOLOGO"]

# ✅ Apenas psicólogos podem realizar consultas
def is_psicologo(user):
    return user.is_authenticated and user.tipo_usuario == "PSICOLOGO"

# 🔹 Permite que todos os profissionais de saúde vejam os agendamentos
@login_required
@user_passes_test(is_profissional_saude)
def listar_agendamentos(request):
    """Lista os agendamentos, visível para todos os profissionais de saúde"""
    agendamentos = Agendamento.objects.all().order_by("-data")
    return render(request, "agendamentos/listar_agendamentos.html", {"agendamentos": agendamentos})

# 🔹 Apenas psicólogos podem criar consultas
@login_required
@user_passes_test(is_psicologo)
def adicionar_consulta(request):
    """Permite que o psicólogo adicione uma nova consulta"""

    # Obtém os agendamentos do profissional logado
    agendamentos = Agendamento.objects.filter(psicologo=request.user, status="Em andamento")

    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.profissional = request.user
            consulta.save()
            messages.success(request, "Consulta criada com sucesso!")
            return redirect("listar_consultas")

    else:
        form = ConsultaForm()

    return render(
        request,
        "consultas/adicionar_consulta.html",  
        {"form": form, "agendamentos": agendamentos},
    )

# 🔹 Apenas psicólogos podem listar suas próprias consultas
@login_required
@user_passes_test(is_psicologo)
def listar_consultas(request):
    """Lista todas as consultas do psicólogo logado"""
    consultas = Consulta.objects.filter(profissional=request.user).order_by("-data_consulta")

    return render(
        request,
        "consultas/listar_consultas.html",
        {"consultas": consultas}
    )

# 🔹 Apenas psicólogos podem atender consultas
@login_required
@user_passes_test(is_psicologo)
def realizar_consulta(request, agendamento_id):
    """
    Permite que o psicólogo realize uma consulta para um paciente agendado.
    Obtém o agendamento e cria ou recupera a consulta correspondente.
    """
    # Obtém o psicólogo logado
    psicologo = request.user

    # Obtém o agendamento garantindo que o psicólogo seja o responsável
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, psicologo=psicologo)

    # Cria ou obtém a consulta associada ao agendamento
    consulta, created = Consulta.objects.get_or_create(
        paciente=agendamento.paciente,            
        profissional=psicologo,                
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
                agendamento.status = "Concluído"  # Atualiza o status do agendamento
                agendamento.save()  # Salva a alteração no banco de dados
            
            consulta.save()
            messages.success(request, "Consulta concluída com sucesso!")
            return redirect("listar_agendamentos")
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, "consultas/realizar_consulta.html", {
        "form": form,
        "consulta": consulta,
        "agendamento": agendamento
    })
