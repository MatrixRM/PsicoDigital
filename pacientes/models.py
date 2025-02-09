from django.db import models

class Paciente(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    cep = models.CharField(max_length=9, blank=True, null=True)  # Corrigindo para incluir o campo CEP
    logradouro = models.CharField(max_length=150, blank=True, null=True)
    numero_casa = models.CharField(max_length=10, blank=True, null=True)  # Corrigindo para incluir o campo número da casa
    bairro = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
