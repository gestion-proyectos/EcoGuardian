from pprint import pprint
import requests
#from flask_login import login_required login_user, current_user
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from configBd import *
import markupsafe, requests
#import markupsafe, requests, bcrypt

# Crear un Blueprint
vistaverincenidos = Blueprint('idvistaverincendios', __name__, template_folder='templates')
 
@vistaverincenidos.route('/ver_incendios', methods=['GET', 'POST'])

def vista_verincenidos():


    return render_template('ver_incendios.html')