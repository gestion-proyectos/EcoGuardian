from flask import Blueprint, render_template, request, flash, redirect, url_for
from configBd import *
from control.ControlConexion import ControlConexion
from flask_login import current_user

vistaeditarcondiciones = Blueprint('idvistaeditarcondiciones', __name__, template_folder='templates')

@vistaeditarcondiciones.route('/editar_condiciones', methods=['GET', 'POST'])
def editar_condiciones():
    datos = None
    if request.method == 'POST':
        condiciones = request.form.getlist('perfil_salud')
        condiciones_pg = '{' + ','.join(condiciones) + '}'
        try:
            conexion = ControlConexion()
            conexion.abrirBd(serv, usua, passw, bdat, port)
            sql = "UPDATE usuarios SET perfil_salud=%s WHERE id_usuario=%s"
            conexion.ejecutarComandoSql(sql, [condiciones_pg, current_user.id])
            conexion.cerrarBd()
            flash('Condiciones de salud actualizadas.', 'success')
        except Exception as e:
            print(f"[ERROR] Error al actualizar condiciones: {str(e)}")
            flash('Error al actualizar condiciones.', 'error')
        return redirect(url_for('idvistaeditarcondiciones.editar_condiciones'))
    # Cargar datos actuales
    try:
        conexion = ControlConexion()
        conexion.abrirBd(serv, usua, passw, bdat, port)
        sql = "SELECT perfil_salud FROM usuarios WHERE id_usuario=%s"
        resultado = conexion.ejecutarSelect(sql, [current_user.id])
        if resultado and len(resultado) > 0:
            datos = resultado[0]
            def pg_array_to_list(val):
                if not val or val == '{}' or val is None:
                    return []
                if isinstance(val, list):
                    return val
                return [x.strip() for x in val.strip('{}').split(',') if x.strip()]
            datos['perfil_salud'] = pg_array_to_list(datos.get('perfil_salud'))
        conexion.cerrarBd()
    except Exception as e:
        print(f"[ERROR] Error al cargar condiciones: {str(e)}")
    return render_template('editar_condiciones.html', datos=datos, active_tab='condiciones')