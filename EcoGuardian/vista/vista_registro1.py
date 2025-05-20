from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
from control.ControlConexion import *

# Crear un Blueprint
vistaregistro1 = Blueprint('idvistaregistro1', __name__, template_folder='templates')
 
@vistaregistro1.route('/registro1', methods=['GET', 'POST'])
def vista_registro1():
    if request.method == 'POST':
        condiciones = request.form.getlist('condiciones')
        estilo_vida = request.form.getlist('estilo_vida')
        # Recuperar datos del primer paso
        nombre = session.get('registro_nombre')
        correo = session.get('registro_correo')
        password = session.get('registro_password')
        print('Datos de sesión:', nombre, correo, password)
        print('Condiciones:', condiciones)
        print('Estilo de vida:', estilo_vida)
        if not (nombre and correo and password):
            flash('Faltan datos del registro. Intenta de nuevo.', 'error')
            return redirect(url_for('idvistaregistro.vista_registro'))
        try:
            conexion = ControlConexion()
            conexion.abrirBd(serv, usua, passw, bdat, port)
            sql = "INSERT INTO usuarios (nombre, correo, contrasena, perfil_salud, estilo_vida) VALUES (%s, %s, %s, %s, %s)"
            conexion.ejecutarComandoSql(sql, [nombre, correo, password, condiciones, estilo_vida])
            conexion.cerrarBd()
            # Limpiar datos de sesión
            session.pop('registro_nombre', None)
            session.pop('registro_correo', None)
            session.pop('registro_password', None)
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('idvistalogin.vista_login'))
        except Exception as e:
            print(f"[ERROR] Error al guardar usuario: {str(e)}")
            flash('Error al guardar usuario. Intenta nuevamente.', 'error')
            return render_template('registro1.html')
    return render_template('registro1.html')