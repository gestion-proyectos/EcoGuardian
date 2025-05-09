import unittest
import allure
from main import app
from flask import session
import time
import random

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

class AuthTests(BaseTestCase):
    def get_unique_email(self):
        """Genera un correo único usando timestamp"""
        return f"test_{int(time.time())}@test.com"

    @allure.title("Prueba de registro completo") #pasa
    @allure.description("Verifica el proceso completo de registro en dos pasos")
    def test_registro_completo(self):
        # Generar correo único
        test_email = self.get_unique_email()
        
        # Paso 1: Registro inicial
        response = self.app.post('/registro', data={
            'nombre': 'Usuario Test',
            'correo': test_email,
            'password': 'test123',
            'confirmar_password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'condiciones', response.data)  # Verifica que estamos en la página de condiciones

        # Paso 2: Registro de condiciones y estilo de vida
        response = self.app.post('/registro1', data={
            'condiciones': ['Problemas respiratorios'],
            'estilo_vida': ['Deportista al aire libre']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro exitoso', response.data)

    @allure.title("Prueba de login exitoso") #pasa
    @allure.description("Verifica que un usuario pueda iniciar sesión correctamente")
    def test_login_exitoso(self):
        # Generar correo único
        test_email = self.get_unique_email()
        
        # Primero registramos un usuario
        # Paso 1: Registro inicial
        response = self.app.post('/registro', data={
            'nombre': 'Usuario Test',
            'correo': test_email,
            'password': 'test123',
            'confirmar_password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Paso 2: Registro de condiciones y estilo de vida
        response = self.app.post('/registro1', data={
            'condiciones': ['Problemas respiratorios'],
            'estilo_vida': ['Deportista al aire libre']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Intentamos hacer login
        response = self.app.post('/login', data={
            'username': test_email,
            'password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenido', response.data)

    @allure.title("Prueba de login fallido") #pasa
    @allure.description("Verifica que el login falle con credenciales incorrectas")
    def test_login_fallido(self):
        response = self.app.post('/login', data={
            'username': 'nonexistent@test.com',
            'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usuario o contrase\xc3\xb1a incorrectos', response.data)

class ReportTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Generar correo único
        self.test_email = f"test_{int(time.time())}@test.com"
        
        # Registrar y hacer login antes de cada prueba
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

    @allure.title("Prueba de reporte de contaminación")
    @allure.description("Verifica el proceso de reportar contaminación")
    def test_reportar_contaminacion(self):
        # Acceder al formulario
        response = self.app.get('/reportar_contaminacion')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reportes de Contaminaci\xc3\xb3n', response.data)

        # Enviar reporte
        response = self.app.post('/reportar_contaminacion', data={
            'calle_afectada': 'Calle 72 #11-86, Bogotá, Colombia',
            'severidad': '3',
            'descripcion': 'Test de contaminación'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reporte de contaminaci\xc3\xb3n registrado exitosamente', response.data)

    @allure.title("Prueba de reporte de incendio")
    @allure.description("Verifica el proceso de reportar incendio")
    def test_reportar_incendio(self):
        # Acceder al formulario
        response = self.app.get('/reportar_incendio')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reportar Incendio', response.data)

        # Enviar reporte
        response = self.app.post('/reportar_incendio', data={
            'calle_afectada': 'Calle 72 #11-86, Bogotá, Colombia',
            'severidad': '3',
            'descripcion': 'Test de incendio'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reporte de incendio registrado exitosamente', response.data)

    @allure.title("Prueba de reporte de polen")
    @allure.description("Verifica el proceso de reportar polen")
    def test_reportar_polen(self):
        # Acceder al formulario
        response = self.app.get('/reportar_polen')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reportar Polen', response.data)

        # Enviar reporte
        response = self.app.post('/reportar_polen', data={
            'calle_afectada': 'Calle 72 #11-86, Bogotá, Colombia',
            'severidad': '2',
            'descripcion': 'Test de polen'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reporte de polen registrado exitosamente', response.data)

class ProfileTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Generar correo único
        self.test_email = f"test_{int(time.time())}@test.com"
        
        # Registrar y hacer login antes de cada prueba
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

    @allure.title("Prueba de edición de perfil")
    @allure.description("Verifica que se pueda editar el perfil del usuario")
    def test_editar_perfil(self):
        response = self.app.post('/editar_perfil', data={
            'nombre': 'Usuario Modificado',
            'correo': self.test_email,
            'form_type': 'datos'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Perfil actualizado correctamente', response.data)

    @allure.title("Prueba de edición de condiciones")
    @allure.description("Verifica que se puedan editar las condiciones de salud")
    def test_editar_condiciones(self):
        response = self.app.post('/editar_perfil', data={
            'form_type': 'condiciones',
            'perfil_salud': ['asmático', 'Alergico al polen']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Condiciones de salud actualizadas', response.data)

    @allure.title("Prueba de edición de estilo de vida")
    @allure.description("Verifica que se pueda editar el estilo de vida")
    def test_editar_estilo(self):
        response = self.app.post('/editar_estilo', data={
            'form_type': 'estilo',
            'estilo_vida': ['camina', 'deportista_al_aire_libre']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Estilo de vida actualizado', response.data)

if __name__ == '__main__':
    unittest.main() 