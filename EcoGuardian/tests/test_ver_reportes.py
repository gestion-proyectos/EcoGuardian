from main import app
from flask import session
import time, random, requests, unittest, allure, json
from unittest.mock import patch
from vista.vistareportarcontamincacion import registrar_reporte, geocodificar_direccion
from vista.vistalogin import load_user

class BaseTestCase(unittest.TestCase):
    def get_unique_email(self):
        """Genera un correo único usando timestamp y un número aleatorio"""
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        return f"test_{timestamp}_{random_num}@test.com"

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

class TestVistaVerPolen(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Generar correo único y registrar usuario
        self.test_email = self.get_unique_email()
        self.app.post('/registro', data={
            'nombre': 'Usuario Test',
            'correo': self.test_email,
            'password': 'test123',
            'confirmar_password': 'test123'
        })
        self.app.post('/registro1', data={
            'condiciones': ['Problemas respiratorios'],
            'estilo_vida': ['Deportista al aire libre']
        })
        self.app.post('/login', data={
            'username': self.test_email,
            'password': 'test123'
        })

    @allure.title("Prueba de vista de polen")
    @allure.description("Verifica que se pueda acceder a la vista de polen")
    @allure.label("severity", "normal")
    def test_vista_polen(self):
        response = self.app.get('/ver_polen')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Polen', response.data)

    @allure.title("Prueba de vista de polen sin autenticación")
    @allure.description("Verifica que se pueda acceder a la vista sin estar autenticado")
    @allure.label("severity", "normal")
    def test_vista_polen_sin_autenticacion(self):
        self.app.get('/logout')
        response = self.app.get('/ver_polen')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Polen', response.data)

    @allure.title("Prueba de reacción a reporte de polen autenticado")
    @allure.description("Verifica que se pueda reaccionar a un reporte estando autenticado")
    @allure.label("severity", "normal")
    def test_reaccion_polen_autenticado(self):
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva',
            'comentario': 'Test de reacción a polen'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')


class TestVistaVerContaminacion(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Generar correo único y registrar usuario
        self.test_email = self.get_unique_email()
        self.app.post('/registro', data={
            'nombre': 'Usuario Test',
            'correo': self.test_email,
            'password': 'test123',
            'confirmar_password': 'test123'
        })
        self.app.post('/registro1', data={
            'condiciones': ['Problemas respiratorios'],
            'estilo_vida': ['Deportista al aire libre']
        })
        self.app.post('/login', data={
            'username': self.test_email,
            'password': 'test123'
        })

    @allure.title("Prueba de vista de contaminación")
    @allure.description("Verifica que se pueda acceder a la vista de contaminación")
    @allure.label("severity", "normal")
    def test_vista_contaminacion(self):
        response = self.app.get('/ver_contaminacion')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contaminaci\xc3\xb3n', response.data)


    @allure.title("Prueba de reacción a reporte de contaminación autenticado")
    @allure.description("Verifica que se pueda reaccionar a un reporte estando autenticado")
    @allure.label("severity", "normal")
    def test_reaccion_contaminacion_autenticado(self):
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva',
            'comentario': 'Test de reacción a contaminación'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')

class TestVistaVerIncendios(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Generar correo único y registrar usuario
        self.test_email = self.get_unique_email()
        self.app.post('/registro', data={
            'nombre': 'Usuario Test',
            'correo': self.test_email,
            'password': 'test123',
            'confirmar_password': 'test123'
        })
        self.app.post('/registro1', data={
            'condiciones': ['Problemas respiratorios'],
            'estilo_vida': ['Deportista al aire libre']
        })
        self.app.post('/login', data={
            'username': self.test_email,
            'password': 'test123'
        })

    @allure.title("Prueba de vista de incendios")
    @allure.description("Verifica que se pueda acceder a la vista de incendios")
    @allure.label("severity", "normal")
    def test_vista_incendios(self):
        response = self.app.get('/ver_incendios')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incendios', response.data)

    @allure.title("Prueba de vista de incendios sin autenticación")
    @allure.description("Verifica que se pueda acceder a la vista sin estar autenticado")
    @allure.label("severity", "normal")
    def test_vista_incendios_sin_autenticacion(self):
        self.app.get('/logout')
        response = self.app.get('/ver_incendios')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incendios', response.data)

    @allure.title("Prueba de reacción a reporte de incendio autenticado")
    @allure.description("Verifica que se pueda reaccionar a un reporte estando autenticado")
    @allure.label("severity", "normal")
    def test_reaccion_incendio_autenticado(self):
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva',
            'comentario': 'Test de reacción a incendio'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')

