from django.contrib import admin
from django.urls import path, include
from home.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('usuario.urls')),
    path("home/", home, name="home"),
]