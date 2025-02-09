from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("O nome de usuário deve ser definido")
        if not email:
            raise ValueError("O e-mail deve ser definido")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("tipo_usuario", "ADMIN")  # Superusuário sempre será ADMIN

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário deve ter is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ("SECRETARIA", "Secretária"),
        ("PROFISSIONAL_SAUDE", "Profissional de Saúde"),
        ("PSICOLOGO", "Psicólogo"),  
        ("ADMIN", "Administrador"),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default="SECRETARIA")

    # ✅ Campos extras para profissionais de saúde
    crp = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Número do Conselho de Psicologia
    especialidade = models.CharField(max_length=255, blank=True, null=True)

    # ✅ Corrige o erro de conflito com grupos e permissões
    groups = models.ManyToManyField(Group, related_name="custom_usuario_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_usuario_permissions", blank=True)

    # ✅ Adiciona o gerenciador de usuários
    objects = UsuarioManager()

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"