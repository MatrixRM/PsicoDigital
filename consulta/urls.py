from django.urls import path
from .views import listar_consultas, realizar_consulta, adicionar_consulta

urlpatterns = [
    path("listar/", listar_consultas, name="listar_consultas"),  # Nova rota para listar consultas
   path("realizar/<int:agendamento_id>/", realizar_consulta, name="realizar_consulta"),  # 🔹 Corrigido!
    path("adicionar/", adicionar_consulta, name="adicionar_consulta"),
]
