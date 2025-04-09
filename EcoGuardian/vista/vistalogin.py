from pprint import pprint
import requests
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe

# Crear un Blueprint
vistalogin = Blueprint('idvistalogin', __name__, template_folder='templates')

@vistalogin.route('/login', methods=['GET', 'POST'])
def vista_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Debug prints
        print(f"[DEBUG] Intento de login - Usuario: {username}")

        if username and password:
            # Autenticación exitosa
            session['username'] = username
            flash('¡Bienvenido! Has iniciado sesión correctamente.', 'success')
            print(f"[DEBUG] Login exitoso - Usuario: {username}")
            return redirect(url_for('home.vista_home'))
        else:
            flash('Por favor, ingresa usuario y contraseña.', 'error')
            print("[DEBUG] Fallo en login - Faltan credenciales")

    return render_template('login.html')
