from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistainiciarruta = Blueprint('idvistainiciarruta', __name__, template_folder='templates')
 
@vistainiciarruta.route('/iniciar_ruta', methods=['GET', 'POST'])

def vista_iniciarruta():


    return render_template('iniciar_ruta.html')