from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from home.views import home

def index(request):
    return render(request, "index.html")

def registrar(request):
    if request.method == 'GET':
        return render(request, 'registrar.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return render(request, "modal_cadastro_usuario_falha.html")
          
        
        else:
            user = User.objects.create_user(username=username, email=email, password=senha)
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso')

    return render(request, 'registrar.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)

            return redirect(home)
        else:
            return HttpResponse('Usuário ou senha inválidos')

@login_required
def plataforma(request):
    if request.user.is_authenticated:
        return render(request, "home.html")

