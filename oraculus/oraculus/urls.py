from django.contrib import admin
from django.urls import path, include
from home.views import home
from usuario.views import index
from django.contrib.auth import views as auth_views
from inserir_analise.views import inserir_analise, post_inserir_analise, delete_inserir_analise
from recomendar_colheita.views import recomendar_colheita
from acessar_dados.views import acessar_dados
from resultado.views import resultado

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include('usuario.urls')),
    path("home/", home, name="home"),
    path("", index, name="index"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),

    path("inserir_analise/", inserir_analise, name="inserir_analise"),
    path("recomendar_colheita/", recomendar_colheita, name="recomendar_colheita"),
    path("acessar_dados/", acessar_dados, name="acessar_dados"),

    path("resultado/", resultado, name="resultado"),

    #botar as urls do crud de colheita aqui
    path("acessar_dados/", post_inserir_analise, name="post_inserir_analise"),
    path("acessar_dados/<int:id>", delete_inserir_analise, name="delete_inserir_analise"),

]
