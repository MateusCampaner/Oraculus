from django.test import TestCase
from django.urls import reverse
from analise.models import Analise, ConfiguracaoAlgoritmo
from django.contrib.auth.models import User

class SalvarConfiguracaoAlgoritmoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='1234')

    def test_salvar_novo_registro_configuracao_modelo(self):
        """Caso de Teste 1: Salvamento de um novo registro de configuração de modelo"""

        dados_post = {
            'username': 'teste',
            'qtdTeste': '0.25',
            'qtdVizinhos': '5',
            'algoritmo': 'auto',
            'pesos': 'uniform',
            'acuracia': '97.63',
        }

        response = self.client.post(reverse('salvar_algoritmo'), data=dados_post)

        self.assertRedirects(response, reverse('configura_algoritmo'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Modelo salvo com sucesso")

        usuario = User.objects.filter(username='teste').first()
        configuracao = ConfiguracaoAlgoritmo.objects.filter(usuario=usuario).first()

        self.assertIsNotNone(configuracao)
        self.assertEqual(configuracao.qtdTeste, 0.25)
        self.assertEqual(configuracao.qtdVizinhos, 5)
        self.assertEqual(configuracao.algoritmo, 'auto')
        self.assertEqual(configuracao.pesos, 'uniform')
        self.assertAlmostEqual(configuracao.acuracia, 97.63)

    def setUp(self):

        self.configuracao = ConfiguracaoAlgoritmo.objects.create(
            usuario_id=1,
            qtdTeste=0.25,
            qtdVizinhos=5,
            algoritmo='auto',
            pesos='uniform',
            acuracia=97.636
        )

    def test_excluir_registro_configuracao_modelo(self):
        """Caso de Teste 3: Exclusão de um registro de dados de configuração de modelo"""

        configuracao_id = self.configuracao.id
        response = self.client.post(reverse('delete_modelo'))
        configuracao_existente = ConfiguracaoAlgoritmo.objects.filter(id=configuracao_id).exists()

        self.assertFalse(configuracao_existente)

        self.assertRedirects(response, reverse('configura_algoritmo'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Registro de configuração de modelo excluído com sucesso")


class SalvarAnaliseSoloTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='1234')

    def test_salvar_novo_registro_analise_solo(self):
        """Caso de Teste 2: Salvamento de um novo registro de análise de solo"""

        dados_post = {
            'id_modelo': 1,
            'username': 'teste',
            'N': '20',
            'P': '40',
            'K': '60',
            'Temperatura': '25.5',
            'Umidade': '70',
            'pH': '6.9',
            'Chuva': '100',
            'colheita_prevista': 'Manga',
        }

        response = self.client.post(reverse('salvar_analises'), data=dados_post)
        self.assertRedirects(response, reverse('resultado'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Análise salva com sucesso")

        usuario = User.objects.get(username='teste')
        analise = Analise.objects.filter(usuario=usuario).first()

        self.assertIsNotNone(analise)
        self.assertEqual(analise.N, 20)
        self.assertEqual(analise.P, 40)
        self.assertEqual(analise.K, 60)
        self.assertAlmostEqual(analise.Temperatura, 25.5) 
        self.assertAlmostEqual(analise.Umidade, 70)
        self.assertAlmostEqual(analise.pH, 6.9)
        self.assertAlmostEqual(analise.Chuva, 100)
        self.assertEqual(analise.Colheita, 'Manga')
        self.assertEqual(analise.usuario, usuario)

    def setUp(self):
        # Criando um registro de Análise para teste
        self.analise = Analise.objects.create(
            N=20,
            P=40,
            K=60,
            Temperatura=25.5,
            Umidade=70,
            pH=6.9,
            Chuva=100,
            Colheita='Milho',
            usuario_id=1
        )

    def test_excluir_registro_analise_solo(self):
        """Caso de Teste 4: Exclusão de um registro de dados de análise de solo"""

        analise_id = self.analise.id

        response = self.client.post(reverse('delete_analise'))
        analise_existente = Analise.objects.filter(id=analise_id).exists()

        self.assertFalse(analise_existente)
        self.assertRedirects(response, reverse('resultado'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Registro de análise de solo excluído com sucesso")


