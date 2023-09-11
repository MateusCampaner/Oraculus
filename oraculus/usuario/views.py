from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required

def registrar(request):
    if request.method == 'GET':
        return render(request, 'registrar.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Usuário já cadastrado')
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return HttpResponse('Usuário castrado com sucesso')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)

            return HttpResponse('Autenticado com sucesso')
        else:
            return HttpResponse('Usuário ou senha inválidos')

@login_required(login_url='/auth/login/')
def plataforma(request):
    if request.user.is_authenticated:
        return HttpResponse('Plataforma')
