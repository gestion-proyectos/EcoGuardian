from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests

from control.ControlConexion import ControlConexion

# Crear un Blueprint
vistaregistro = Blueprint('idvistaregistro', __name__, template_folder='templates')
 
@vistaregistro.route('/registro', methods=['GET', 'POST'])
def vista_registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        confirmar_password = request.form.get('confirmar_password')

        # Validar que las contraseñas coincidan
        if password != confirmar_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('registro.html')

        # Validar que el correo no exista
        try:
            conexion = ControlConexion()
            conexion.abrirBd(serv, usua, passw, bdat, port)
            sql = "SELECT * FROM usuarios WHERE correo = %s"
            resultado = conexion.ejecutarSelect(sql, [correo])
            if resultado and len(resultado) > 0:
                flash('El correo ya está registrado.', 'error')
                conexion.cerrarBd()
                return render_template('registro.html')
            # Guardar datos en sesión temporal para el siguiente paso
            session['registro_nombre'] = nombre
            session['registro_correo'] = correo
            session['registro_password'] = password
            conexion.cerrarBd()
            return redirect(url_for('idvistaregistro1.vista_registro1'))
        except Exception as e:
            print(f"[ERROR] Error en registro: {str(e)}")
            flash('Error al registrar. Intenta nuevamente.', 'error')
            return render_template('registro.html')
    return render_template('registro.html')