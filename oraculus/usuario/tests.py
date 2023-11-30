from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class UsuarioTestCase(TestCase):
    def setUp(self):
        #Criação de usuário de teste
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testeUsuario',
            email='testeUsuario@email.com',
            password='teste1234'
        )

    def test_criacao_usuario(self):
        """Caso de teste 1: Cadastro bem-sucedido de usuário"""

        novo_usuario = self.User.objects.create_user(
            username='testeUsuario1',
            email='testeUsuario1@email.com',
            password='teste12345'
        )
        self.assertIsNotNone(novo_usuario)
        self.assertEqual(novo_usuario.username, 'testeUsuario1')
        self.assertEqual(novo_usuario.email, 'testeUsuario1@email.com')
        self.assertTrue(novo_usuario.check_password('teste12345'))
        self.assertTrue(novo_usuario.is_active)
        self.assertFalse(novo_usuario.is_staff)
        self.assertFalse(novo_usuario.is_superuser)

    
    def test_email_valido(self):
        """Caso de teste 2: Cadastro com email inválido"""

        novo_usuario = self.User(username='testeUsuarioEmail', email='testeUsuarioemail', password='teste1234')
        with self.assertRaises(ValidationError):
            novo_usuario.full_clean()

        novo_usuario.email = 'testeUsuario@email.com'
        try:
            novo_usuario.full_clean()
        except ValidationError:
            self.fail("Email inválido")

    def test_criacao_usuario_sem_senha(self):
        """Caso de teste 3: Tentativa de criar conta sem senha"""
        try:
            self.User.objects.create_user(
                username='usuarioSemSenha',
                email='usuarioSemSenha@email.com',
                password=''  
            )
        except ValidationError:
            pass 
        else:
            self.fail("Não foi possível criar o usuário, insira uma senha")

    def test_criacao_usuario_com_senha_fraca(self):
        """Caso de teste 4: Tentativa de criar conta com senha fraca"""
        senha_fraca = '1234'
        try:
            self.User.objects.create_user(
                username='usuarioSenhaFraca',
                email='usuarioSenhafraca@email.com',
                password=senha_fraca
            )
        except ValidationError as e:
            self.assertIn("Senha fraca", str(e))
        else:
            self.fail("Não foi possível criar o usuário com senha fraca, insira uma senha maior e com mais caracteres")

    def test_criacao_usuario_duplicado(self):
        """Caso de teste 5: Tentativa de criar conta duplicada"""
        try:
            self.User.objects.create_user(
                username='testeUsuario',
                email='testeUsuario@email.com',
                password='teste1234'
            )
        except IntegrityError as e:
            self.assertIn("Usuário único", str(e)) 
        else:
            self.fail("Não foi possível criar o usuário, já existe um usuário com esse Username")
