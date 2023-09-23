from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")

@login_required
def ajuda(request):
    return render(request, "ajuda.html")

@login_required
def sobre(request):
    return render(request, "sobre.html")