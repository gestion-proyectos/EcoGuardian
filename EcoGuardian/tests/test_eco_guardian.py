import unittest
import allure
from main import app
from flask import session

class TestEcoGuardian(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @allure.title("Prueba de inicio de sesión exitoso")
    @allure.description("Verifica que un usuario pueda iniciar sesión correctamente")
    @allure.label("severity", "high")
    def test_login_success(self):
        with self.app as client:
            response = client.post('/login', data={
                'username': 'test_user',
                'password': 'test_password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bienvenido', response.data)

    @allure.title("Prueba de acceso a la página de inicio")
    @allure.description("Verifica que la página de inicio se cargue correctamente")
    @allure.label("severity", "medium")
    def test_home_page(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'test_user'
            response = client.get('/home')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'test_user', response.data)

    @allure.title("Prueba de cierre de sesión")
    @allure.description("Verifica que el usuario pueda cerrar sesión correctamente")
    @allure.label("severity", "high")
    def test_logout(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'test_user'
            response = client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('username', session)

    @allure.title("Prueba de registro de usuario")
    @allure.description("Verifica que un nuevo usuario pueda registrarse correctamente")
    @allure.label("severity", "high")
    def test_user_registration(self):
        with self.app as client:
            response = client.post('/registro', data={
                'username': 'new_user',
                'email': 'new_user@test.com',
                'password': 'new_password',
                'confirm_password': 'new_password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Registro exitoso', response.data)

    @allure.title("Prueba de acceso a rutas protegidas")
    @allure.description("Verifica que las rutas protegidas redirijan al login cuando no hay sesión")
    @allure.label("severity", "medium")
    def test_protected_routes(self):
        with self.app as client:
            response = client.get('/home', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'login', response.data.lower())

if __name__ == '__main__':
    unittest.main()
