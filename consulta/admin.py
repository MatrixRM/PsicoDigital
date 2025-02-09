from django.contrib import admin
from .models import Consulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "profissional", "data_consulta", "horario_consulta", "status")
    list_filter = ("status", "data_consulta", "profissional")  # Certifique-se de que esses campos existem
    search_fields = ("paciente__username", "profissional__username")
    ordering = ("-data_consulta", "-horario_consulta")

