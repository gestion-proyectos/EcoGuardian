from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistaeditarperfil = Blueprint('idvistaeditarperfil', __name__, template_folder='templates')
 
@vistaeditarperfil.route('/editar_perfil', methods=['GET', 'POST'])
#@vistaprueba.route('/Desktop4', methods=['GET', 'POST'])

def vista_editar_perfil():


   return render_template('editar_perfil.html')