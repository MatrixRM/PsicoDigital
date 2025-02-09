from django import forms
from .models import Agendamento
from pacientes.models import Paciente
from usuarios.models import Usuario

class AgendamentoForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        label="Paciente",
        empty_label="Selecione um Paciente",
        required=True
    )

    psicologo = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(tipo_usuario="PSICOLOGO"),
        label="Psicólogo",
        empty_label="Selecione um Psicólogo",
        required=True
    )

    status = forms.ChoiceField(
        choices=Agendamento.STATUS_CHOICES,  # Aqui referenciamos a tupla corretamente
        label="Status",
        required=True
    )

    class Meta:
        model = Agendamento
        fields = ['paciente', 'psicologo', 'data', 'hora', 'observacoes', 'status']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
