from django.contrib import admin
from django.urls import path, include
from home.views import home
from usuario.views import index
from django.contrib.auth import views as auth_views
from inserir_analise.views import inserir_analise, post_inserir_analise
from recomendar_colheita.views import recomendar_colheita
from acessar_dados.views import acessar_dados, delete_analises
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

    #Crud de colheita aqui
    path("post_inserir_analise/", post_inserir_analise, name="post_inserir_analise"),
    path("delete_inserir_analise/<int:id>/", delete_analises, name="delete_inserir_analise"),

]
