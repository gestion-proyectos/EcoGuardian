from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistareportarpolen = Blueprint('idvistareportarpolen', __name__, template_folder='templates')
 
@vistareportarpolen.route('/reportar_polen', methods=['GET', 'POST'])

def vista_reportarpolen():


    return render_template('reportar_polen.html')