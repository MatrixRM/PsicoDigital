from django.urls import path
from .views import listar_agendamentos, criar_agendamento, editar_agendamento, excluir_agendamento

urlpatterns = [
    path('', listar_agendamentos, name='listar_agendamentos'),
    path('criar/', criar_agendamento, name='criar_agendamento'),
    path('editar/<int:agendamento_id>/', editar_agendamento, name='editar_agendamento'),
    path('excluir/<int:agendamento_id>/', excluir_agendamento, name='excluir_agendamento'),
]
