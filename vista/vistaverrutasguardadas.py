from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistaverrutasguardadas = Blueprint('idvistaverrutasguardadas', __name__, template_folder='templates')
 
@vistaverrutasguardadas.route('/ver_rutas_guardadas', methods=['GET', 'POST'])

def vista_verrutasguardadas():


    return render_template('ver_rutas_guardadas.html')