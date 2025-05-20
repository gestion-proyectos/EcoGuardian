from main import app
from flask import session
import time, random, requests, unittest, allure
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

class AuthTests(BaseTestCase):
    def get_unique_email(self):
        """Genera un correo único usando timestamp"""
        return f"test_{int(time.time())}@test.com"

    @allure.title("Prueba de login exitoso")
    @allure.description("Verifica que un usuario pueda iniciar sesión correctamente")
    @allure.label("severity", "critical")
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
        # Verificamos elementos que sabemos que están en la página de inicio
        self.assertIn(b'EcoGuardian', response.data)
        self.assertIn(b'EcoEventos', response.data)
        self.assertIn(b'Rutas', response.data)
        self.assertIn(b'Reportar', response.data)

    @allure.title("Prueba de login fallido")
    @allure.description("Verifica que el login falle con credenciales incorrectas")
    @allure.label("severity", "critical")
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
    @allure.label("severity", "normal")
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
    @allure.label("severity", "normal")
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
    @allure.label("severity", "normal")
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
    @allure.label("severity", "minor")
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
    @allure.label("severity", "minor")
    def test_editar_condiciones(self):
        response = self.app.post('/editar_perfil', data={
            'form_type': 'condiciones',
            'perfil_salud': ['asmático', 'Alergico al polen']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Condiciones de salud actualizadas', response.data)

    @allure.title("Prueba de edición de estilo de vida")
    @allure.description("Verifica que se pueda editar el estilo de vida")
    @allure.label("severity", "minor")
    def test_editar_estilo(self):
        response = self.app.post('/editar_estilo', data={
            'form_type': 'estilo',
            'estilo_vida': ['camina', 'deportista_al_aire_libre']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Estilo de vida actualizado', response.data)

class TestRegistrarReporte(unittest.TestCase):
    @allure.title("Prueba de registro de reporte exitoso")
    @allure.description("Verifica que se pueda registrar un reporte de contaminación correctamente")
    @allure.label("severity", "critical")
    @patch('vista.vistareportarcontamincacion.ControlConexion')
    def test_registrar_reporte_exito(self, mock_conexion):
        # Simular inserción exitosa
        mock_conexion.return_value.ejecutarComandoSql.return_value = True
        
        resultado, mensaje = registrar_reporte('Calle 72', 3, 'Descripción de prueba', 1)
        self.assertTrue(resultado)
        self.assertEqual(mensaje, 'Reporte registrado exitosamente')

    @allure.title("Prueba de registro de reporte con error")
    @allure.description("Verifica el manejo de errores al registrar un reporte de contaminación")
    @allure.label("severity", "critical")
    @patch('vista.vistareportarcontamincacion.ControlConexion')
    def test_registrar_reporte_error(self, mock_conexion):
        # Simular error en la inserción
        mock_conexion.return_value.ejecutarComandoSql.side_effect = Exception("Error de base de datos")
        
        resultado, mensaje = registrar_reporte('Calle 72', 3, 'Descripción de prueba', 1)
        self.assertFalse(resultado)
        self.assertIn('Error', mensaje)

class TestGeocodificarDireccion(unittest.TestCase):
    @allure.title("Prueba de geocodificación exitosa")
    @allure.description("Verifica que se pueda geocodificar una dirección correctamente")
    @allure.label("severity", "critical")
    @patch('vista.vistareportarcontamincacion.requests.get')
    def test_geocodificar_direccion_exito(self, mock_get):
        # Simular respuesta exitosa de Nominatim
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{
            'lat': '4.60971',
            'lon': '-74.08175'
        }]
        
        direccion = "Bogotá, Colombia"
        resultado = geocodificar_direccion(direccion)
        self.assertEqual(resultado, "POINT(-74.08175 4.60971)")

    @allure.title("Prueba de geocodificación sin resultados")
    @allure.description("Verifica el manejo de direcciones que no se pueden geocodificar")
    @allure.label("severity", "critical")
    @patch('vista.vistareportarcontamincacion.requests.get')
    def test_geocodificar_direccion_sin_resultados(self, mock_get):
        # Simular respuesta sin resultados
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        
        direccion = "Dirección inexistente"
        resultado = geocodificar_direccion(direccion)
        self.assertIsNone(resultado)

    @allure.title("Prueba de geocodificación con error de API")
    @allure.description("Verifica el manejo de errores de la API de geocodificación")
    @allure.label("severity", "normal")
    @patch('vista.vistareportarcontamincacion.requests.get')
    def test_geocodificar_direccion_error(self, mock_get):
        # Simular error en la solicitud
        mock_get.return_value.status_code = 500
        
        direccion = "Bogotá, Colombia"
        resultado = geocodificar_direccion(direccion)
        self.assertIsNone(resultado)

    @allure.title("Prueba de geocodificación con dirección con caracteres especiales")
    @allure.description("Verifica que se puedan geocodificar direcciones con caracteres especiales")
    @allure.label("severity", "normal")
    @patch('vista.vistareportarcontamincacion.requests.get')
    def test_geocodificar_direccion_caracteres_especiales(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{
            'lat': '4.60971',
            'lon': '-74.08175'
        }]
        
        direccion = "Calle 72 #11-86, Bogotá, Colombia"
        resultado = geocodificar_direccion(direccion)
        self.assertEqual(resultado, "POINT(-74.08175 4.60971)")

    @allure.title("Prueba de geocodificación con timeout")
    @allure.description("Verifica el manejo de timeouts en la API de geocodificación")
    @allure.label("severity", "critical")
    @patch('vista.vistareportarcontamincacion.requests.get')
    def test_geocodificar_direccion_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        
        direccion = "Bogotá, Colombia"
        resultado = geocodificar_direccion(direccion)
        self.assertIsNone(resultado)

class TestLogin(unittest.TestCase):
    @allure.title("Prueba de carga de usuario exitosa")
    @allure.description("Verifica que se pueda cargar un usuario correctamente")
    @allure.label("severity", "critical")
    @patch('vista.vistalogin.ControlConexion')
    def test_load_user_exito(self, mock_conexion):
        # Simular conexión exitosa a la base de datos
        mock_conexion.return_value.ejecutarSelect.return_value = [{
            'id_usuario': 1,
            'correo': 'test_user@test.com'
        }]
        
        user = load_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.correo, 'test_user@test.com')

    @allure.title("Prueba de carga de usuario no encontrado")
    @allure.description("Verifica el manejo de usuarios que no existen en la base de datos")
    @allure.label("severity", "critical")
    @patch('vista.vistalogin.ControlConexion')
    def test_load_user_no_encontrado(self, mock_conexion):
        # Simular usuario no encontrado
        mock_conexion.return_value.ejecutarSelect.return_value = []
        
        user = load_user(99)
        self.assertIsNone(user)

    @allure.title("Prueba de carga de usuario con datos incompletos")
    @allure.description("Verifica el manejo de usuarios con datos incompletos en la base de datos")
    @allure.label("severity", "critical")
    @patch('vista.vistalogin.ControlConexion')
    def test_load_user_datos_incompletos(self, mock_conexion):
        mock_conexion.return_value.ejecutarSelect.return_value = [{
            'id_usuario': 1
            # Falta el campo 'correo'
        }]
        
        user = load_user(1)
        self.assertIsNone(user)

class TestPerfilIntegracion(BaseTestCase):
    @allure.title("Prueba de integración: Actualización completa de perfil")
    @allure.description("Verifica el flujo completo de actualización de perfil")
    @allure.label("severity", "minor")
    def test_actualizacion_perfil_completa(self):
        # 1. Registrar usuario
        test_email = self.get_unique_email()
        self.app.post('/registro', data={
            'nombre': 'Usuario Test',
            'correo': test_email,
            'password': 'test123',
            'confirmar_password': 'test123'
        })
        self.app.post('/registro1', data={
            'condiciones': ['Problemas respiratorios'],
            'estilo_vida': ['Deportista al aire libre']
        })

        # 2. Login
        self.app.post('/login', data={
            'username': test_email,
            'password': 'test123'
        })

        # 3. Actualizar datos básicos
        response = self.app.post('/editar_perfil', data={
            'nombre': 'Usuario Modificado',
            'correo': test_email,
            'form_type': 'datos'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Perfil actualizado correctamente', response.data)

        # 4. Actualizar condiciones
        response = self.app.post('/editar_perfil', data={
            'form_type': 'condiciones',
            'perfil_salud': ['asmático', 'Alergico al polen']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Condiciones de salud actualizadas', response.data)

        # 5. Actualizar estilo de vida
        response = self.app.post('/editar_estilo', data={
            'form_type': 'estilo',
            'estilo_vida': ['camina', 'deportista_al_aire_libre']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Estilo de vida actualizado', response.data)

        # 6. Verificar cambios
        response = self.app.get('/editar_perfil')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usuario Modificado', response.data)
        self.assertIn(b'asm\xc3\xa1tico', response.data)
        self.assertIn(b'deportista_al_aire_libre', response.data)

class TestApiReaccion(BaseTestCase):
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

    @allure.title("Prueba de reacción exitosa")
    @allure.description("Verifica que se pueda agregar una reacción correctamente")
    @allure.label("severity", "critical")
    def test_agregar_reaccion(self):
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva',
            'comentario': 'Test de reacción'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')
        self.assertIn('id_reaccion', data['data'])

    @allure.title("Prueba de reacción sin autenticación")
    @allure.description("Verifica que no se pueda agregar una reacción sin estar autenticado")
    @allure.label("severity", "critical")
    def test_reaccion_sin_autenticacion(self):
        self.app.get('/logout')
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva'
        })
        self.assertEqual(response.status_code, 401)

    @allure.title("Prueba de obtener comentarios")
    @allure.description("Verifica que se puedan obtener los comentarios de un reporte")
    @allure.label("severity", "normal")
    def test_obtener_comentarios(self):
        # Primero agregamos un comentario
        self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'comentario': 'Test de comentario'
        })
        
        # Luego intentamos obtener los comentarios
        response = self.app.get('/api/comentarios/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')
        self.assertIsInstance(data['comentarios'], list)

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

    @allure.title("Prueba de reacción a reporte de polen sin autenticación")
    @allure.description("Verifica que no se pueda reaccionar sin estar autenticado")
    @allure.label("severity", "critical")
    def test_reaccion_polen_sin_autenticacion(self):
        self.app.get('/logout')
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva',
            'comentario': 'Test de reacción a polen'
        })
        self.assertEqual(response.status_code, 401)

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

    @allure.title("Prueba de vista de contaminación sin autenticación")
    @allure.description("Verifica que se pueda acceder a la vista sin estar autenticado")
    @allure.label("severity", "normal")
    def test_vista_contaminacion_sin_autenticacion(self):
        self.app.get('/logout')
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

    @allure.title("Prueba de reacción a reporte de contaminación sin autenticación")
    @allure.description("Verifica que no se pueda reaccionar sin estar autenticado")
    @allure.label("severity", "critical")
    def test_reaccion_contaminacion_sin_autenticacion(self):
        self.app.get('/logout')
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva',
            'comentario': 'Test de reacción a contaminación'
        })
        self.assertEqual(response.status_code, 401)

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

    @allure.title("Prueba de reacción a reporte de incendio sin autenticación")
    @allure.description("Verifica que no se pueda reaccionar sin estar autenticado")
    @allure.label("severity", "critical")
    def test_reaccion_incendio_sin_autenticacion(self):
        self.app.get('/logout')
        response = self.app.post('/api/reaccion', json={
            'id_reporte': 1,
            'tipo_reaccion': 'positiva',
            'comentario': 'Test de reacción a incendio'
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 