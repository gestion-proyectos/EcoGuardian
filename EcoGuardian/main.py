# main.py
from flask import Flask, redirect, jsonify, request, url_for
from flask import jsonify, request, redirect, url_for
import os
from datetime import timedelta
from configBd import *
from vista.vistalogin import login_manager, load_user
from flask_login import LoginManager

from menu import menu
from vista.vistalogin import vistalogin
from vista.vistaregistro import vistaregistro
from vista.vista_registro1 import vistaregistro1
from vista.vistahome import vistahome
from vista.api_reaccion import api

"""editarperfil"""
from vista.vistaeditarperfil import vistaeditarperfil
from vista.vistaeditarcondiciones import vistaeditarcondiciones
from vista.vistaeditarestilo import vistaeditarestilo

"""EcoEventos"""
from vista.vistavercontaminacion import vistavercontaminacion
from vista.vistaverincendios import vistaverincenidos
from vista.vistaverpolen import vistaverpolen

"""Rutas"""
from vista.vistarutas import vistarutas

"""Reportar"""
from vista.vistareportarincendio import vistareportarincendio
from vista.vistareportarcontamincacion import vistareportarcontamincacion
from vista.vistareportarpolen import vistareportarpolen

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)

# Configurar login_manager
login_manager.init_app(app)
login_manager.login_view = 'idvistalogin.vista_login'
login_manager.user_loader(load_user)

# Registrar los blueprints
app.register_blueprint(menu)  # Este debe ser el primero para que la ruta raíz muestre el menú
app.register_blueprint(vistahome)
app.register_blueprint(vistalogin)

"""Registro"""
app.register_blueprint(vistaregistro)
app.register_blueprint(vistaregistro1)

"""EcoEventos"""
app.register_blueprint(vistavercontaminacion)
app.register_blueprint(vistaverincenidos)
app.register_blueprint(vistaverpolen)

"""Editar perfil"""
app.register_blueprint(vistaeditarperfil)
app.register_blueprint(vistaeditarcondiciones)
app.register_blueprint(vistaeditarestilo)

"""Api"""
app.register_blueprint(api)

@login_manager.unauthorized_handler
def unauthorized_callback():
    # Si la ruta es de la API, devuelve JSON y 401
    if request.path.startswith('/api/'):
        return jsonify({'status': 'error', 'message': 'Usuario no autenticado'}), 401
    # Si no, redirige al login normal
    return redirect(url_for('idvistalogin.vista_login'))

"""Rutas"""
app.register_blueprint(vistarutas)

"""Reportar"""
app.register_blueprint(vistareportarincendio)
app.register_blueprint(vistareportarcontamincacion)
app.register_blueprint(vistareportarpolen)

# Vista de logout
def logout_view(request):
    return redirect('login')

# Vista del menú principal
def vista_menu():
    #código de validación de control de acceso al menú
    return redirect('menu.html') 

if __name__ == '__main__':
    # Corre la aplicación en el modo debug, lo que permitirá
    # la recarga automática del servidor cuando se detecten cambios en los archivos.
    app.run(debug=True)