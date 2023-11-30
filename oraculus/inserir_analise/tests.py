from django.test import TestCase
from django.urls import reverse

class AnaliseSoloTestCase(TestCase):
    def test_analise_solo_insercao_correta(self):
        """Caso de Teste 1: Inserção bem-sucedida de todos os dados de análise de solo"""
        
        dados_analise = {
            'id_modelo' : 1,
            'qtdTeste' : 0.25,
            'qtdVizinhos' : 5,
            'algoritmo' : 'auto',
            'pesos' : 'uniform',
            'acuracia' : 97.636,
            'N' : 20,
            'P' : 40,
            'K' : 60,
            'Temperatura' : 25.5,
            'Umidade' : 70,
            'pH' : 6.9,
            'Chuva' : 100,
        }

        response = self.client.post(reverse('rodar_algoritmo_analise'), data=dados_analise)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resultado.html')
    
    def test_analise_solo_insercao_vazia(self):
        """Caso de Teste 2: Inserção com campo em branco"""

        dados_analise = {
            'id_modelo': 1,
            'qtdTeste': 0.25,
            'qtdVizinhos': 5,
            'algoritmo': 'auto',
            'pesos': 'uniform',
            'acuracia': 97.636,
            'N': 20,
            'P': 40,
            'K': 60,
            'Temperatura': 25.5,
            'Umidade': 70,
            'pH': 6.9,
            'Chuva': '', 
        }

        response = self.client.post(reverse('rodar_algoritmo_analise'), data=dados_analise)
        self.assertRedirects(response, reverse('inserir_analise'))
    
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Por favor, preencha todos os campos obrigatórios")

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn('resultado.html', response)

    def test_analise_solo_insercao_negativa(self):
        """Caso de Teste 3: Inserção com valor negativo"""

        dados_analise = {
            'id_modelo': 1,
            'qtdTeste': 0.25,
            'qtdVizinhos': 5,
            'algoritmo': 'auto',
            'pesos': 'uniform',
            'acuracia': 97.636,
            'N': 20,
            'P': 40,
            'K': 60,
            'Temperatura': 25.5,
            'Umidade': 70,
            'pH': 6.9,
            'Chuva': -100, 
        }

        response = self.client.post(reverse('rodar_algoritmo_analise'), data=dados_analise)
        self.assertRedirects(response, reverse('inserir_analise'))
    
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Valor inválido, os valores não podem ser negativos")

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn('resultado.html', response)

    def test_analise_solo_insercao_ph_invalida(self):
        """Caso de Teste 4: Inserção com pH inválido"""

        dados_analise = {
            'id_modelo': 1,
            'qtdTeste': 0.25,
            'qtdVizinhos': 5,
            'algoritmo': 'auto',
            'pesos': 'uniform',
            'acuracia': 97.636,
            'N': 20,
            'P': 40,
            'K': 60,
            'Temperatura': 25.5,
            'Umidade': 70,
            'pH': 15,
            'Chuva': 100, 
        }

        response = self.client.post(reverse('rodar_algoritmo_analise'), data=dados_analise)
        self.assertRedirects(response, reverse('inserir_analise'))
    
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Valor de pH inválido, insira um valor de 1 a 14")

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn('resultado.html', response)

    def test_analise_solo_insercao_ph_invalida(self):
        """Caso de Teste 5: Inserção com quantidade de chuva em formato inválido"""

        dados_analise = {
            'id_modelo': 1,
            'qtdTeste': 0.25,
            'qtdVizinhos': 5,
            'algoritmo': 'auto',
            'pesos': 'uniform',
            'acuracia': 97.636,
            'N': 20,
            'P': 40,
            'K': 60,
            'Temperatura': 25.5,
            'Umidade': 70,
            'pH': 15,
            'Chuva': 'cem', 
        }

        response = self.client.post(reverse('rodar_algoritmo_analise'), data=dados_analise)
        self.assertRedirects(response, reverse('inserir_analise'))
    
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Valor inválido, valores podem ser somente numéricos")

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn('resultado.html', response)

############################################################################################

from django.test import TestCase
from django.urls import reverse
from django.contrib import messages

class TreinarModeloTestCase(TestCase):
    def test_modelo_algoritmo_salvamento(self):
        """Caso de Uso 1: Salvamento bem-sucedido de um modelo de algoritmo"""

        dados_modelo = {
            'qtdTeste': 25,  
            'qtdVizinhos': 5,
            'algoritmo': 'auto',
            'pesos': 'uniform',
        }

        response = self.client.post(reverse('treinar_algoritmo'), data=dados_modelo)
        self.assertTemplateUsed(response, 'configura_algoritmo.html')

        self.assertIn('knn', response.context)
        self.assertIn('acuracia', response.context) 

        acuracia = response.context['acuracia']
        self.assertGreaterEqual(acuracia, 0)
        self.assertLessEqual(acuracia, 100)

    def test_numero_vizinhos_muito_alto(self):
        """Caso de Uso 2: Número de vizinhos muito alto"""

        dados_modelo = {
            'qtdTeste': 25,  
            'qtdVizinhos': 1000,  
            'algoritmo': 'auto',
            'pesos': 'uniform',
        }

        response = self.client.post(reverse('treinar_algoritmo'), data=dados_modelo)
        self.assertRedirects(response, reverse('configura_algoritmo'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "O valor máximo de Número de Vizinhos é 1650, escolha um valor menor, ou diminua a proporção de Teste / Treino")

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn('configura_algoritmo.html', response)
        

    def test_numero_vizinhos_vazio(self):
        """Caso de Uso 3: Número de vizinhos vazio"""

        dados_modelo = {
            'qtdTeste': 25,  
            'qtdVizinhos': '',  
            'algoritmo': 'auto',
            'pesos': 'uniform',
        }

        response = self.client.post(reverse('treinar_algoritmo'), data=dados_modelo)
        self.assertRedirects(response, reverse('configura_algoritmo'))

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "O Valor mínimo de Número de Vizinhos é 1, escolha um valor maior")

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn('configura_algoritmo.html', response)

    def test_salvar_modelo_sem_executar_treinamento(self):
        """Caso de Uso 4: Tentar salvar o modelo sem executar treinamento"""

        dados_treinamento = {
            'qtdTeste': '',
            'qtdVizinhos': '',
            'algoritmo': '',
            'pesos': '',
        }

        response = self.client.post(reverse('salvar_algoritmo'), data=dados_treinamento)
        self.assertRedirects(response, reverse('configura_algoritmo'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Modelo não treinado, realize um treinamento de modelo para salvar")

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn('configura_algoritmo.html', response)



