from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistaañadirruta = Blueprint('idvistaañadirruta', __name__, template_folder='templates')
 
@vistaañadirruta.route('/añadir_ruta', methods=['GET', 'POST'])

def vista_añadirruta():


    return render_template('añadir_ruta.html')