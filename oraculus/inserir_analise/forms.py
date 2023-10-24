from django import forms
from analise.models import AnaliseSolo, Analise, ConfiguracaoAlgoritmo
from datetime import date

class AnaliseSoloForm(forms.ModelForm):
    class Meta:
        model = AnaliseSolo
        fields = ('usuario', 'data_analise')

    def __init__(self, user, *args, **kwargs):
        super(AnaliseSoloForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].initial = user
        self.fields['data_analise'].initial = date.today()

class AnaliseForm(forms.ModelForm):
    class Meta:
        model = Analise
        fields = ('N', 'P', 'K', 'Temperatura', 'Umidade', 'pH', 'Chuva', 'analiseSolo')

class ConfiguracaoAlgoritmoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoAlgoritmo
        fields = ('qtdTeste', 'qtdVizinhos', 'algoritmo', 'pesos', 'analiseSolo')