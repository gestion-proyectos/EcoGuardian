from flask import Blueprint, render_template, request, flash, redirect, url_for
from configBd import *
from control.ControlConexion import ControlConexion
from flask_login import current_user

vistaeditarestilo = Blueprint('idvistaeditarestilo', __name__, template_folder='templates')

@vistaeditarestilo.route('/editar_estilo', methods=['GET', 'POST'])
def editar_estilo():
    datos = None
    if request.method == 'POST':
        estilo = request.form.getlist('estilo_vida')
        estilo_pg = '{' + ','.join(estilo) + '}'
        try:
            conexion = ControlConexion()
            conexion.abrirBd(serv, usua, passw, bdat, port)
            sql = "UPDATE usuarios SET estilo_vida=%s WHERE id_usuario=%s"
            conexion.ejecutarComandoSql(sql, [estilo_pg, current_user.id])
            conexion.cerrarBd()
            flash('Estilo de vida actualizado.', 'success')
        except Exception as e:
            print(f"[ERROR] Error al actualizar estilo: {str(e)}")
            flash('Error al actualizar estilo.', 'error')
        return redirect(url_for('idvistaeditarestilo.editar_estilo'))
    # Cargar datos actuales
    try:
        conexion = ControlConexion()
        conexion.abrirBd(serv, usua, passw, bdat, port)
        sql = "SELECT estilo_vida FROM usuarios WHERE id_usuario=%s"
        resultado = conexion.ejecutarSelect(sql, [current_user.id])
        if resultado and len(resultado) > 0:
            datos = resultado[0]
            def pg_array_to_list(val):
                if not val or val == '{}' or val is None:
                    return []
                if isinstance(val, list):
                    return val
                return [x.strip() for x in val.strip('{}').split(',') if x.strip()]
            datos['estilo_vida'] = pg_array_to_list(datos.get('estilo_vida'))
        conexion.cerrarBd()
    except Exception as e:
        print(f"[ERROR] Error al cargar estilo: {str(e)}")
    return render_template('editar_estilo.html', datos=datos, active_tab='estilo')