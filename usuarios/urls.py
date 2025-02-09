from django.urls import path
from .views import login_view, logout_view, registrar_usuario

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("registrar/", registrar_usuario, name="registrar_usuario"),

]
