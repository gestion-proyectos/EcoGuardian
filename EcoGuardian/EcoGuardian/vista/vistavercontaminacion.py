from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistavercontaminacion = Blueprint('idvistavercontaminacion', __name__, template_folder='templates')
 
@vistavercontaminacion.route('/ver_contaminacion', methods=['GET', 'POST'])

def vista_vercontaminacion():


    return render_template('ver_contaminacion.html')