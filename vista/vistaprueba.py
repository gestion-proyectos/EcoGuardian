from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistaprueba = Blueprint('idvistaprueba', __name__, template_folder='templates')
 
@vistaprueba.route('/index', methods=['GET', 'POST'])
#@vistaprueba.route('/Desktop4', methods=['GET', 'POST'])

def vista_prueba():


   return render_template('index.html')
#   return render_template('Desktop4.html')