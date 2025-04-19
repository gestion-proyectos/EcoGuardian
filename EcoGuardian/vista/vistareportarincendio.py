from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistareportarincendio = Blueprint('idvistareportarincendio', __name__, template_folder='templates')
 
@vistareportarincendio.route('/reportar_incendio', methods=['GET', 'POST'])

def vista_reportarincendio():


    return render_template('reportar_incendio.html')