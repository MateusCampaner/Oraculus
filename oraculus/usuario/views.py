from django.shortcuts import render, redirect
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

        if username == '':
            messages.error(request, "Username vazio, insira um Username")
            return render(request, 'registrar.html')
        
        elif email == '':
            messages.error(request, "Email vazio, insira um Email")
            return render(request, 'registrar.html')
        
        elif senha == '':
            messages.error(request, "Senha vazia, insira uma Senha")
            return render(request, 'registrar.html')
        
        user = User.objects.filter(username=username).first()

        if user:
            messages.error(request, "Usuário já existe")

            return render(request, 'registrar.html')
        
          
        else:
            user = User.objects.create_user(username=username, email=email, password=senha)
            user.save()

            messages.success(request, "Usuário cadastrado com sucesso")

            return render(request, 'registrar.html')

    #return render(request, 'registrar.html')

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
            messages.error(request, "Usuário ou senha inválidos")

            return render(request, 'login.html')

@login_required
def plataforma(request):
    if request.user.is_authenticated:
        return render(request, "home.html")

