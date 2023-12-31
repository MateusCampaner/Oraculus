from django.contrib import admin
from django.urls import path, include
from home.views import home, ajuda, sobre
from usuario.views import index
from django.contrib.auth import views as auth_views
from inserir_analise.views import inserir_analise, rodar_algoritmo_analise, treinar_algoritmo, configura_algoritmo, salvar_algoritmo, selecionar_modelo
from recomendar_colheita.views import recomendar_colheita, enviar_colheita, calcular_valores, gerar_relatorio_colheita
from acessar_dados.views import acessar_dados, delete_analises, visualizar_analise, delete_modelos, acessar_dados_analise, acessar_dados_modelo, visualizar_modelo
from visualizar_analise.views import delete_analise, gerar_relatorio_analise
from resultado.views import resultado, salvar_analises

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
    path("rodar_algoritmo_analise/", rodar_algoritmo_analise, name="rodar_algoritmo_analise"),
    path("delete_inserir_analise/<int:id>/", delete_analises, name="delete_inserir_analise"),
    path("treinar_algoritmo", treinar_algoritmo, name="treinar_algoritmo"),
    path("configura_algoritmo", configura_algoritmo, name="configura_algoritmo"),
    path("salvar_algoritmo", salvar_algoritmo, name="salvar_algoritmo"),
    path("selecionar_modelo", selecionar_modelo, name="selecionar_modelo"),

    #Resultado
    path("salvar_analises/", salvar_analises, name="salvar_analises"),

    #Crud de Acessar Dados
    path("acessar_dados_analise", acessar_dados_analise, name="acessar_dados_analise"),
    path("acessar_dados_modelo", acessar_dados_modelo, name="acessar_dados_modelo"),
    path("visualizar_analise/<int:id>/", visualizar_analise, name="visualizar_analise"),
    path("delete_analise/<int:id>/", delete_analise, name="delete_analise"),
    path("gerar_relatorio_analise", gerar_relatorio_analise, name="gerar_relatorio_analise"),
    path("visualizar_modelo/<int:id>/", visualizar_modelo, name="visualizar_modelo"),
    path("delete_modelos/<int:id>/", delete_modelos, name="delete_modelos"),

    #Recomendar Colheita
    path('enviar_colheita/', enviar_colheita, name='enviar_colheita'),
    path('calcular_valores/', calcular_valores, name='calcular_valores'),
    path('gerar_relatorio_colheita/', gerar_relatorio_colheita, name='gerar_relatorio_colheita'), 
]
