from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Agendamento
from .forms import AgendamentoForm
from usuarios.permissions import is_secretaria_ou_profissional_saude, pode_gerenciar_agendamento, is_psicologo

@login_required
@user_passes_test(is_secretaria_ou_profissional_saude)
def listar_agendamentos(request):
    """Lista os agendamentos para profissionais de saúde"""
    agendamentos = Agendamento.objects.exclude(id=None).order_by("-data", "-hora")
    
    if not agendamentos:
        messages.warning(request, "Nenhum agendamento encontrado!")

    return render(request, "agendamentos/listar_agendamentos.html", {"agendamentos": agendamentos})



# ✅ Criar um novo agendamento
@login_required
@user_passes_test(is_secretaria_ou_profissional_saude)

def criar_agendamento(request):
    """Permite criar um novo agendamento selecionando paciente e psicólogo"""

    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            
            # Garantir que o status seja atribuído corretamente
            if not agendamento.status:
                agendamento.status = "PENDENTE"  # Se o status não for informado, atribui PENDENTE

            agendamento.save()
            messages.success(request, "Agendamento criado com sucesso!")
            return redirect("listar_agendamentos")
        else:
            messages.error(request, 'Erro ao criar agendamento.')
    else:
        form = AgendamentoForm()

    return render(request, "agendamentos/criar_agendamento.html", {"form": form})


# ✅ Editar um agendamento
@login_required
def editar_agendamento(request, agendamento_id):
    """Permite que apenas psicólogos editem seus próprios agendamentos e secretárias editem qualquer agendamento"""

    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if not pode_gerenciar_agendamento(request.user, agendamento):
        messages.error(request, "Você não tem permissão para editar este agendamento.")
        return redirect("listar_agendamentos")

    if request.method == "POST":
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Agendamento atualizado com sucesso!")
            return redirect("listar_agendamentos")
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(request, "agendamentos/editar_agendamento.html", {"form": form, "agendamento": agendamento})


# ✅ Excluir um agendamento
@login_required
def excluir_agendamento(request, agendamento_id):
    """Permite que psicólogos excluam seus próprios agendamentos e secretárias excluam qualquer agendamento"""

    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if not pode_gerenciar_agendamento(request.user, agendamento):
        messages.error(request, "Você não tem permissão para excluir este agendamento.")
        return redirect("listar_agendamentos")

    if request.method == "POST":
        agendamento.delete()
        messages.success(request, "Agendamento excluído com sucesso!")
        return redirect("listar_agendamentos")

    return render(request, "agendamentos/confirmar_exclusao.html", {"agendamento": agendamento})
