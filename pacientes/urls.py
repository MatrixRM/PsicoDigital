from django.urls import path
from .views import listar_pacientes, cadastrar_paciente, editar_paciente, listar_pacientes, excluir_paciente

urlpatterns = [
    path("", listar_pacientes, name="listar_pacientes"),
    path("cadastrar/", cadastrar_paciente, name="cadastrar_paciente"),
    path("editar/<int:paciente_id>/", editar_paciente, name="editar_paciente"),
    path('listar/', listar_pacientes, name='listar_pacientes'),
    path('excluir/<int:paciente_id>/', excluir_paciente, name='excluir_paciente'),
]
