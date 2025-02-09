from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cpf', 'nome', 'sobrenome', 'data_nascimento', 'telefone', 'whatsapp', 'email', 
                  'cep', 'logradouro', 'numero_casa', 'bairro', 'estado', 'cidade']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(XX) XXXXX-XXXX'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '(XX) XXXXX-XXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'}),
            'cep': forms.TextInput(attrs={'placeholder': 'XXXXX-XXX'}),
            'logradouro': forms.TextInput(attrs={'placeholder': 'Rua, Avenida...'}),
            'numero_casa': forms.TextInput(attrs={'placeholder': 'Número'}),
            'bairro': forms.TextInput(attrs={'placeholder': 'Bairro'}),
            'estado': forms.TextInput(attrs={'placeholder': 'Estado'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Cidade'}),
        }

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone and not telefone.isdigit():
            raise forms.ValidationError("O telefone deve conter apenas números.")
        if telefone and (len(telefone) < 10 or len(telefone) > 11):
            raise forms.ValidationError("Número de telefone inválido. Use o formato: 999999999 ou 99999999999.")
        return telefone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        paciente_id = self.instance.id  # Obtém o ID do paciente caso seja uma edição

        # Verifica se existe outro paciente com o mesmo e-mail
        if Paciente.objects.filter(email=email).exclude(id=paciente_id).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado para outro paciente!")
        
        return email