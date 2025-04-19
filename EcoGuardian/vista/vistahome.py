from flask import Blueprint, render_template, session, redirect, url_for, flash

vistahome = Blueprint('home', __name__, template_folder='templates')

@vistahome.route('/home')
def vista_home():
    usuario = session.get('username', 'Invitado')  # Obtener usuario de la sesión
    return render_template('home.html', usuario=usuario)


@vistahome.route('/logout')
def logout():
    username = session.get('username', 'Invitado')
    session.pop('username', None)
    print(f"El usuario {username} ha cerrado sesión exitosamente")
    flash(f"¡Hasta luego {username}! Has cerrado sesión exitosamente", 'info')
    return redirect(url_for('idvistalogin.vista_login'))
