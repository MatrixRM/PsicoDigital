from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Agendamento
from .forms import AgendamentoForm
from usuarios.models import Usuario


# ✅ Função para verificar se o usuário pode ver agendamentos
def pode_ver_agendamentos(user):
    """Permite que Psicólogos, Secretárias e Profissionais de Saúde visualizem os agendamentos."""
    return user.is_authenticated and user.tipo_usuario in ["SECRETARIA", "PROFISSIONAL_SAUDE", "PSICOLOGO"]


# ✅ Função para verificar se o usuário pode gerenciar um agendamento (editar/excluir)
def pode_gerenciar_agendamento(user, agendamento):
    """
    - Psicólogos podem gerenciar apenas seus próprios agendamentos.
    - Secretárias podem gerenciar qualquer agendamento.
    """
    return user.tipo_usuario == "SECRETARIA" or (user.tipo_usuario == "PSICOLOGO" and agendamento.psicologo == user)


# ✅ View para listar os agendamentos
@login_required
@user_passes_test(pode_ver_agendamentos)
def listar_agendamentos(request):
    """Lista os agendamentos disponíveis para o usuário logado."""

    if request.user.tipo_usuario == "SECRETARIA":
        agendamentos = Agendamento.objects.all().order_by("-data", "-hora")  # Secretárias veem todos os agendamentos
    else:
        agendamentos = Agendamento.objects.filter(psicologo=request.user).order_by("-data", "-hora")  # Psicólogos veem apenas os seus

    return render(request, "agendamentos/listar_agendamentos.html", {"agendamentos": agendamentos})


@login_required
def criar_agendamento(request):
    """Permite criar um novo agendamento selecionando paciente e psicólogo"""
    
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # Verifique o que está sendo enviado no formulário
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




# ✅ View para editar um agendamento
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



# ✅ View para excluir um agendamento
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
