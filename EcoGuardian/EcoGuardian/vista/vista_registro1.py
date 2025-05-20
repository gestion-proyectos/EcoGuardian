from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistaregistro1 = Blueprint('idvistaregistro1', __name__, template_folder='templates')
 
@vistaregistro1.route('/registro1', methods=['GET', 'POST'])

def vista_registro1():


    return render_template('registro1.html')