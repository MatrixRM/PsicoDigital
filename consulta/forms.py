from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["anotacoes_atendimento", "pontos_atencao"]
        widgets = {
            "anotacoes_atendimento": forms.Textarea(attrs={"rows": 3}),
            "pontos_atencao": forms.Textarea(attrs={"rows": 3}),
        }
