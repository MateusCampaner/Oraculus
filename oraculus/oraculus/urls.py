from django.contrib import admin
from django.urls import path, include
from home.views import home, ajuda, sobre
from usuario.views import index
from django.contrib.auth import views as auth_views
from inserir_analise.views import inserir_analise, rodar_algoritmo_analise, salvar_algoritmo_analise, rodar_analise
from recomendar_colheita.views import recomendar_colheita, enviar_colheita, calcular_valores, gerar_relatorio_colheita
from acessar_dados.views import acessar_dados, delete_analises, visualizar_analise
from visualizar_analise.views import delete_analise, gerar_relatorio_analise
from resultado.views import resultado

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include('usuario.urls')),
    path("home/", home, name="home"),
    path("", index, name="index"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),

    path("ajuda", ajuda, name="ajuda"),
    path("sobre", sobre, name="sobre"),

    path("inserir_analise/", inserir_analise, name="inserir_analise"),
    path("recomendar_colheita/", recomendar_colheita, name="recomendar_colheita"),
    path("acessar_dados/", acessar_dados, name="acessar_dados"),

    path("resultado/", resultado, name="resultado"),

    #Crud de Inserir Análise

    path("salvar_algoritmo_analise/", salvar_algoritmo_analise, name="salvar_algoritmo_analise"),
    path("rodar_algoritmo_analise/", rodar_algoritmo_analise, name="rodar_algoritmo_analise"),
    path("delete_inserir_analise/<int:id>/", delete_analises, name="delete_inserir_analise"),
    path("rodar_analise/", rodar_analise, name="rodar_analise"),
    
    #Crud de Acessar Dados
    path("visualizar_analise/<int:id>/", visualizar_analise, name="visualizar_analise"),
    path("delete_analise/<int:id>/", delete_analise, name="delete_analise"),
    path("gerar_relatorio_analise", gerar_relatorio_analise, name="gerar_relatorio_analise"),

    #Recomendar Colheita
    path('enviar_colheita/', enviar_colheita, name='enviar_colheita'),
    path('calcular_valores/', calcular_valores, name='calcular_valores'),
    path('gerar_relatorio_colheita/', gerar_relatorio_colheita, name='gerar_relatorio_colheita'), 

]
