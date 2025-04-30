from pprint import pprint
import requests
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from configBd import *
import markupsafe
from control.ControlConexion import ControlConexion

# Crear un Blueprint
vistalogin = Blueprint('idvistalogin', __name__, template_folder='templates')

# Configurar LoginManager
login_manager = LoginManager()
login_manager.login_view = 'idvistalogin.vista_login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.correo = username

@login_manager.user_loader
def load_user(user_id):
    try:
        conexion = ControlConexion()
        conexion.abrirBd(serv, usua, passw, bdat, port)
        
        #sql = "SELECT id, usuario FROM usuarios WHERE id = %s"
        sql = "SELECT id_usuario, correo FROM usuarios WHERE id_usuario = %s"
        resultado = conexion.ejecutarSelect(sql, [user_id])
        
        if resultado and len(resultado) > 0:
            #return User(resultado[0]['id'], resultado[0]['usuario'])
            return User(resultado[0]['id_usuario'], resultado[0]['correo'])
        return None
        
    except Exception as e:
        print(f"[ERROR] Error al cargar usuario: {str(e)}")
        return None
    finally:
        if 'conexion' in locals():
            conexion.cerrarBd()

@vistalogin.route('/login', methods=['GET', 'POST'])
def vista_login():
    if request.method == 'POST':
        #usuario = request.form.get('username')
        correo = request.form.get('username')
        contrasena = request.form.get('password')
        
        # Debug prints
        #print(f"[DEBUG] Intento de login - Usuario: {usuario}")
        print(f"[DEBUG] Intento de login - Usuario: {correo}")

        #if usuario and contrasena:
        if correo and contrasena:
            # Verificar credenciales en la base de datos
            try:
                # Crear conexión a la base de datos
                conexion = ControlConexion()
                conexion.abrirBd(serv, usua, passw, bdat, port)
                
                # Consultar usuario en la base de datos
                sql = "SELECT id_usuario, correo, contrasena FROM usuarios WHERE correo = %s"
                resultado = conexion.ejecutarSelect(sql, [correo])
                
                if resultado and len(resultado) > 0:
                    # Autenticación exitosa
                    #user = User(resultado[0]['id'], resultado[0]['usuario'])
                    user = User(resultado[0]['id_usuario'], resultado[0]['correo'])
                    login_user(user)
                    flash('¡Bienvenido! Has iniciado sesión correctamente.', 'success')
                    #print(f"[DEBUG] Login exitoso - Usuario: {usuario}")
                    print(f"[DEBUG] Login exitoso - Usuario: {correo}")
                    return redirect(url_for('home.vista_home'))
                else:
                    flash('Usuario o contraseña incorrectos.', 'error')
                    print("[DEBUG] Fallo en login - Credenciales incorrectas")
                
                conexion.cerrarBd()
                
            except Exception as e:
                print(f"[ERROR] Error al verificar credenciales: {str(e)}")
                flash('Error al verificar credenciales. Por favor, intente nuevamente.', 'error')
        else:
            flash('Por favor, ingresa usuario y contraseña.', 'error')
            print("[DEBUG] Fallo en login - Faltan credenciales")

    return render_template('login.html')

@vistalogin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('idvistalogin.vista_login'))
