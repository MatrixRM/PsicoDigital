from django.db import models
from usuarios.models import Usuario

class Agendamento(models.Model):
    paciente = models.ForeignKey("pacientes.Paciente", on_delete=models.CASCADE)
    
    psicologo = models.ForeignKey(
        Usuario,  # Alteração: Usa Usuario, já que PROFISSIONAL_SAUDE é um tipo de usuário
        on_delete=models.CASCADE,
        limit_choices_to={"tipo_usuario": "PSICOLOGO"}  # Apenas usuários psicólogos
    )

    data = models.DateField()
    hora = models.TimeField()
    observacoes = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = [
        ("Em andamento", "Em andamento"),
        ("Concluído", "Concluído"),
        ("Cancelado", "Cancelado"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Em andamento")

    def __str__(self):
        return f"{self.paciente.nome} - {self.data} {self.hora}"
