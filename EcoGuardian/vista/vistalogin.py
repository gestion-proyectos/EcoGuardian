from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from configBd import *
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

@login_manager.unauthorized_handler
def unauthorized_callback():
    if request.is_json or request.path.startswith('/api/'):
        return jsonify({
            'status': 'error',
            'message': 'Usuario no autenticado'
        }), 401
    return redirect(url_for('idvistalogin.vista_login'))

@login_manager.user_loader
def load_user(user_id):
    try:
        conexion = ControlConexion()
        conexion.abrirBd(serv, usua, passw, bdat, port)
        
        sql = "SELECT id_usuario, correo FROM usuarios WHERE id_usuario = %s"
        resultado = conexion.ejecutarSelect(sql, [user_id])
        
        if resultado and len(resultado) > 0:
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
        correo = request.form.get('username')
        contrasena = request.form.get('password')
        print(f"[DEBUG] Intento de login - Usuario: {correo}")

        if correo and contrasena:
            try:
                conexion = ControlConexion()
                conexion.abrirBd(serv, usua, passw, bdat, port)
                
                sql = "SELECT id_usuario, correo, contrasena FROM usuarios WHERE correo = %s"
                resultado = conexion.ejecutarSelect(sql, [correo])
                
                if resultado and len(resultado) > 0:
                    if contrasena == resultado[0]['contrasena']:
                        user = User(resultado[0]['id_usuario'], resultado[0]['correo'])
                        login_user(user)
                        print(f"[DEBUG] Login exitoso - Usuario: {correo}")
                        return redirect(url_for('home.vista_home'))
                    else:
                        flash('Usuario o contraseña incorrectos.', 'error')
                        print("[DEBUG] Fallo en login - Contraseña incorrecta")
                else:
                    flash('Usuario o contraseña incorrectos.', 'error')
                    print("[DEBUG] Fallo en login - Usuario no encontrado")
                
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
