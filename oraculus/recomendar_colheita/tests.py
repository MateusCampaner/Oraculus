from django.test import TestCase
from django.urls import reverse

class RecomendarColheitaTestCase(TestCase):
    def test_recomendar_colheita_dados_estatisticos(self):
        """Caso de Teste 1: Escolha de colheita e retorno dos dados"""

        colheita = 'Arroz'
        
        dados_post = {'colheita': colheita}
        response = self.client.post(reverse('calcular_valores'), data=dados_post)

        self.assertEqual(response.status_code, 200)

        self.assertIn('colheita', response.context)
        self.assertEqual(response.context['colheita'], colheita)

        self.assertIn('media_n', response.context)
        self.assertIn('media_p', response.context)
        self.assertIn('media_pH', response.context)

    
    def test_recomendacao_sem_escolher_colheita(self):
        """Caso de Teste 2: Recomendação sem escolher colheita"""

        dados_post = {} 
        response = self.client.post(reverse('calcular_valores'), data=dados_post)

 
        self.assertRedirects(response, reverse('recomendar_colheita'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Selecione uma colheita para gerar um relatório")

        self.assertNotIn('colheita', response.context)
        self.assertNotIn('media_n', response.context)

    def test_gerar_relatorio_sem_escolher_colheita(self):
        """Caso de Teste 3: Gerar Relatório sem escolher colheita"""

        dados_post = {}  
        response = self.client.post(reverse('gerar_relatorio_colheita'), data=dados_post)

        self.assertRedirects(response, reverse('recomendar_colheita'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Selecione uma colheita para gerar um relatório")

