from django.contrib.auth import get_user_model

Usuario = get_user_model()


def is_profissional_saude(user):
    """Verifica se o usuário logado é um profissional de saúde"""
    return user.is_authenticated and user.tipo_usuario in ["PROFISSIONAL_SAUDE", "PSICOLOGO"]


def is_psicologo(user):
    """Verifica se o usuário logado é um psicólogo"""
    return user.is_authenticated and user.tipo_usuario == "PSICOLOGO"



def pode_ver_agendamentos(user):
    """Permite que Psicólogos, Secretárias e Profissionais de Saúde visualizem os agendamentos."""
    return user.is_authenticated and user.tipo_usuario in ["SECRETARIA", "PROFISSIONAL_SAUDE", "PSICOLOGO"]


def pode_gerenciar_agendamento(user, agendamento):
    """
    - Psicólogos podem gerenciar apenas seus próprios agendamentos.
    - Secretárias podem gerenciar qualquer agendamento.
    """
    return user.tipo_usuario == "SECRETARIA" or (user.tipo_usuario == "PSICOLOGO" and agendamento.psicologo == user)


#  Função para verificar se o usuário é Secretária ou Profissional de Saúde
def is_secretaria_ou_profissional_saude(user):
    return user.is_authenticated and user.tipo_usuario in "SECRETARIA, PROFISSIONAL_SAUDE, PSICOLOGO"