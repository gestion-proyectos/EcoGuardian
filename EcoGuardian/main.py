# main.py
from flask import Flask, render_template, redirect, session, flash, send_file, request, url_for
import os, io, xlsxwriter, requests
from datetime import timedelta
from configBd import *

from menu import menu
from vista.vistalogin import vistalogin
from vista.vistaregistro import vistaregistro
from vista.vista_registro1 import vistaregistro1
from vista.vistahome import vistahome
from vista.vistaprueba import vistaprueba
from vista.vistaeditarperfil import vistaeditarperfil


app = Flask(__name__)
app.secret_key = os.urandom(24)
#app.secret_key = 'b14ca5898a4e4133bbce2ea2315a1916'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)

# Registrar los blueprints
app.register_blueprint(menu)  # Este debe ser el primero para que la ruta raíz muestre el menú
app.register_blueprint(vistalogin)
app.register_blueprint(vistaregistro)
app.register_blueprint(vistaregistro1)
app.register_blueprint(vistahome)
app.register_blueprint(vistaprueba)
app.register_blueprint(vistaeditarperfil)

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