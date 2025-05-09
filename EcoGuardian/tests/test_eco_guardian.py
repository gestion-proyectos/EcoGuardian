import unittest
import allure
from main import app
from flask import session

class AuthTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @allure.title("Prueba de inicio de sesión exitoso")
    @allure.description("Verifica que un usuario pueda iniciar sesión correctamente")
    @allure.label("severity", "high")
    def test_login_success(self):
        # Registro previo
        self.app.post('/registro', data={
            'username': 'test_user@test.com',
            'password': 'test_password',
            'confirm_password': 'test_password'
        }, follow_redirects=True)
        # Login
        response = self.app.post('/login', data={
            'username': 'test_user@test.com',
            'password': 'test_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenido', response.data)

    @allure.title("Prueba de cierre de sesión")
    @allure.description("Verifica que el usuario pueda cerrar sesión correctamente")
    @allure.label("severity", "high")
    def test_logout(self):
        with self.app.session_transaction() as sess:
            sess['username'] = 'test_user'
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('username', session)

class HomeTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @allure.title("Prueba de acceso a la página de inicio")
    @allure.description("Verifica que la página de inicio se cargue correctamente")
    @allure.label("severity", "medium")
    def test_home_page(self):
        with self.app.session_transaction() as sess:
            sess['username'] = 'test_user'
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_user', response.data)

class ReportTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_reportar_contaminacion_get(self):
        """Prueba que la vista de reportar contaminación cargue correctamente (GET)."""
        response = self.app.get('/reportar_contaminacion')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reportar Contaminacion', response.data)

    def test_reportar_contaminacion_post(self):
        """Prueba que se pueda enviar un reporte de contaminación (POST)."""
        response = self.app.post('/reportar_contaminacion', data={
            'calle_afectada': 'Calle Falsa 123',
            'severidad': '3',
            'descripcion': 'Prueba de contaminación'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reporte de contaminacion', response.data)

    def test_reportar_incendio_get(self):
        """Prueba que la vista de reportar incendio cargue correctamente (GET)."""
        response = self.app.get('/reportar_incendio')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reportar Incendio', response.data)

    def test_reportar_incendio_post(self):
        """Prueba que se pueda enviar un reporte de incendio (POST)."""
        response = self.app.post('/reportar_incendio', data={
            'calle_afectada': 'Calle Fuego 456',
            'severidad': '5',
            'descripcion': 'Prueba de incendio'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reporte de incendio', response.data)

    def test_reportar_polen_get(self):
        """Prueba que la vista de reportar polen cargue correctamente (GET)."""
        response = self.app.get('/reportar_polen')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reportar Polen', response.data)

    def test_reportar_polen_post(self):
        """Prueba que se pueda enviar un reporte de polen (POST)."""
        response = self.app.post('/reportar_polen', data={
            'calle_afectada': 'Calle Verde 789',
            'severidad': '2',
            'descripcion': 'Prueba de polen'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reporte de polen', response.data)

if __name__ == '__main__':
    unittest.main()
