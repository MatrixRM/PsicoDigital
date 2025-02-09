from django.db import models
from usuarios.models import Usuario
from pacientes.models import Paciente  # Importa o modelo Paciente

class Consulta(models.Model):
    STATUS_CHOICES = [
        ("EM_ANDAMENTO", "Em andamento"),
        ("CONCLUIDO", "Concluído"),
    ]

    paciente = models.ForeignKey(
        Paciente,  # Agora referenciamos o modelo correto
        on_delete=models.CASCADE,
        related_name="consultas_paciente"
    )

    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="consultas_profissional",
        limit_choices_to={"tipo_usuario": "PROFISSIONAL_SAUDE"}
    )

    data_consulta = models.DateField()
    horario_consulta = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="EM_ANDAMENTO")

    anotacoes_atendimento = models.TextField(blank=True, null=True)
    pontos_atencao = models.TextField(blank=True, null=True)

    def __str__(self):
        # Como o modelo Paciente já implementa __str__ retornando "nome sobrenome",
        # basta referenciá-lo diretamente.
        return f"{self.paciente} - {self.data_consulta} às {self.horario_consulta}"
