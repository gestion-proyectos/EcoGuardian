from flask import Blueprint, render_template, flash
from configBd import *
from control.ControlConexion import ControlConexion

# Crear un Blueprint
vistaverpolen = Blueprint('idvistaverpolen', __name__, template_folder='templates')
 
@vistaverpolen.route('/ver_polen', methods=['GET', 'POST'])

def vista_verpolen():
    control_con = ControlConexion()
    conn = control_con.abrirBd(
        servidor=serv,
        usuario=usua,
        password=passw,
        db=bdat,
        puerto=port
    )
    
    if conn is None:
        flash('Error al conectar con la base de datos. Por favor, verifica la configuración.', 'error')
        return render_template('ver_polen.html', reportes=[])

    # Primero, verificar si hay datos en la tabla
    sql_check = """
        SELECT COUNT(*) as total 
        FROM reportes_ambientales 
        WHERE tipo_evento = 'Polen';
    """
    count_result = control_con.ejecutarSelect(sql_check)
    print("Número total de polen en la base de datos:", count_result[0]['total'] if count_result else 0)

    sql = """
        SELECT 
            id_reporte,
            tipo_evento,
            severidad,
            descripcion,
            fecha_reporte,
            calle_afectada,
            usuario_reporta,
            ST_X(ST_Transform(ubicacion, 4326)) AS lon,
            ST_Y(ST_Transform(ubicacion, 4326)) AS lat
        FROM reportes_ambientales
        WHERE tipo_evento = 'Polen'
        AND ubicacion IS NOT NULL;
    """

    reportes = control_con.ejecutarSelect(sql)
    #print("Reportes encontrados:", reportes)  # Debug print

    control_con.cerrarBd()

    if reportes is False:
        flash('Error al obtener los datos de la base de datos.', 'error')
        return render_template('ver_polen.html', reportes=[])

    # Convertir las fechas a string para JSON
    for reporte in reportes:
        if 'fecha_reporte' in reporte:
            reporte['fecha_reporte'] = reporte['fecha_reporte'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"Reporte procesado - ID: {reporte.get('id_reporte')}, Lat: {reporte.get('lat')}, Lon: {reporte.get('lon')}")

    return render_template('ver_polen.html', reportes=reportes)