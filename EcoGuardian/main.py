# main.py
from flask import Flask, render_template, redirect, session, flash, send_file, request, url_for
import os, io, xlsxwriter, requests
from datetime import timedelta
from .configBd import *
from .vista.vistalogin import login_manager

from EcoGuardian.menu import menu
from EcoGuardian.vista.vistalogin import vistalogin
from EcoGuardian.vista.vistaregistro import vistaregistro
from EcoGuardian.vista.vista_registro1 import vistaregistro1
from EcoGuardian.vista.vistahome import vistahome
from EcoGuardian.vista.vistaeditarperfil import vistaeditarperfil

"""EcoEventos"""
from EcoGuardian.vista.vistavercontaminacion import vistavercontaminacion
from EcoGuardian.vista.vistaverincendios import vistaverincenidos
from EcoGuardian.vista.vistaverpolen import vistaverpolen

"""Rutas"""
from EcoGuardian.vista.vistaverrutasguardadas import vistaverrutasguardadas
from EcoGuardian.vista.vistainiciarruta import vistainiciarruta
from EcoGuardian.vista.vistaañadirruta import vistaañadirruta

"""Reportar"""
from EcoGuardian.vista.vistareportarincendio import vistareportarincendio
from EcoGuardian.vista.vistareportarcontamincacion import vistareportarcontamincacion
from EcoGuardian.vista.vistareportarpolen import vistareportarpolen

app = Flask(__name__)
app.secret_key = os.urandom(24)
#app.secret_key = 'b14ca5898a4e4133bbce2ea2315a1916'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)

# Inicializar LoginManager
login_manager.init_app(app)

# Registrar los blueprints
app.register_blueprint(menu)  # Este debe ser el primero para que la ruta raíz muestre el menú
app.register_blueprint(vistalogin)
app.register_blueprint(vistaregistro)
app.register_blueprint(vistaregistro1)
app.register_blueprint(vistahome)
app.register_blueprint(vistaeditarperfil)
app.register_blueprint(vistavercontaminacion)
app.register_blueprint(vistaverincenidos)
app.register_blueprint(vistaverpolen)

app.register_blueprint(vistaverrutasguardadas)
app.register_blueprint(vistainiciarruta)
app.register_blueprint(vistaañadirruta)

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