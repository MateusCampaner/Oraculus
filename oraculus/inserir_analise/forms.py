from django import forms
from analise.models import AnaliseSolo, Analise, ConfiguracaoAlgoritmo
from datetime import date
from django.utils import timezone

class AnaliseSoloForm(forms.ModelForm):
    class Meta:
        model = AnaliseSolo
        fields = ('data_analise',)  # Apenas incluímos o campo 'data_analise' no formulário

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtenha o usuário da keyword argument
        super(AnaliseSoloForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['usuario'].initial = user  # Preencha o campo 'usuario' com o usuário logado
        self.fields['data_analise'].initial = timezone.now().date()  # Preencha o campo 'data_analise' com a data atual

class AnaliseForm(forms.ModelForm):
    class Meta:
        model = Analise
        fields = ('N', 'P', 'K', 'Temperatura', 'Umidade', 'pH', 'Chuva')

class ConfiguracaoAlgoritmoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoAlgoritmo
        fields = ('qtdTeste', 'qtdVizinhos', 'algoritmo', 'pesos')