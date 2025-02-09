from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home  # Importe a view home

urlpatterns = [
    path("", home, name="home"),  # Agora a URL principal "/" leva para a página inicial
    path("login/", auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("admin/", admin.site.urls),
    path("pacientes/", include("pacientes.urls")),
    path("agendamentos/", include("agendamentos.urls")),
    # path("psicologos/", include("psicologos.urls")),
    path("usuarios/", include("usuarios.urls")), 
    path("consultas/", include("consulta.urls")),
]
