from flask import Blueprint, render_template, session, redirect, url_for

vistahome = Blueprint('home', __name__, template_folder='templates')

@vistahome.route('/home')
def vista_home():
    usuario = session.get('username', 'Invitado')  # Obtener usuario de la sesión
    return render_template('home.html', usuario=usuario)


@vistahome.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('idvistalogin.vista_login'))
