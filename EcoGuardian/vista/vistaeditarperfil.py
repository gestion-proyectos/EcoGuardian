from flask import Blueprint, render_template, request, flash
from configBd import *

# Crear un Blueprint
vistaeditarperfil = Blueprint('idvistaeditarperfil', __name__, template_folder='templates')
 
@vistaeditarperfil.route('/editar_perfil', methods=['GET', 'POST'])

def vista_editar_perfil():
    from control.ControlConexion import ControlConexion
    from flask_login import current_user
    datos = None
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        try:
            conexion = ControlConexion()
            conexion.abrirBd(serv, usua, passw, bdat, port)
            if form_type == 'datos':
                nombre = request.form.get('nombre')
                correo = request.form.get('correo')
                password = request.form.get('password')
                confirmar_password = request.form.get('confirmar_password')
                if password and password != confirmar_password:
                    flash('Las contraseñas no coinciden.', 'error')
                else:
                    if password:
                        sql = "UPDATE usuarios SET nombre=%s, correo=%s, contrasena=%s WHERE id_usuario=%s"
                        conexion.ejecutarComandoSql(sql, [nombre, correo, password, current_user.id])
                    else:
                        sql = "UPDATE usuarios SET nombre=%s, correo=%s WHERE id_usuario=%s"
                        conexion.ejecutarComandoSql(sql, [nombre, correo, current_user.id])
                    flash('Perfil actualizado correctamente.', 'success')
            elif form_type == 'condiciones':
                condiciones = request.form.getlist('perfil_salud')
                condiciones_pg = '{' + ','.join(condiciones) + '}'
                sql = "UPDATE usuarios SET perfil_salud=%s WHERE id_usuario=%s"
                conexion.ejecutarComandoSql(sql, [condiciones_pg, current_user.id])
                flash('Condiciones de salud actualizadas.', 'success')
            elif form_type == 'estilo':
                estilo = request.form.getlist('estilo_vida')
                estilo_pg = '{' + ','.join(estilo) + '}'
                sql = "UPDATE usuarios SET estilo_vida=%s WHERE id_usuario=%s"
                conexion.ejecutarComandoSql(sql, [estilo_pg, current_user.id])
                flash('Estilo de vida actualizado.', 'success')
            conexion.cerrarBd()
        except Exception as e:
            print(f"[ERROR] Error al actualizar perfil: {str(e)}")
            flash('Error al actualizar perfil.', 'error')
    # Cargar datos actuales
    try:
        conexion = ControlConexion()
        conexion.abrirBd(serv, usua, passw, bdat, port)
        sql = "SELECT nombre, correo, perfil_salud, estilo_vida FROM usuarios WHERE id_usuario=%s"
        resultado = conexion.ejecutarSelect(sql, [current_user.id])
        if resultado and len(resultado) > 0:
            datos = resultado[0]
            # Convierte los campos de string PostgreSQL a lista de Python para los checkboxes
            def pg_array_to_list(val):
                if not val or val == '{}' or val is None:
                    return []
                if isinstance(val, list):
                    return val
                return [x.strip() for x in val.strip('{}').split(',') if x.strip()]
            datos['perfil_salud'] = pg_array_to_list(datos.get('perfil_salud'))
            datos['estilo_vida'] = pg_array_to_list(datos.get('estilo_vida'))
        conexion.cerrarBd()
    except Exception as e:
        print(f"[ERROR] Error al cargar datos de perfil: {str(e)}")
    return render_template('editar_perfil.html', datos=datos, active_tab='datos')