from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from configBd import *
from control.ControlConexion import ControlConexion
import requests
from flask_login import login_required, current_user
from urllib.parse import quote

# Crear un Blueprint
vistareportarincendio = Blueprint('idvistareportarincendio', __name__, template_folder='templates')

def geocodificar_direccion(direccion):
    try:
        # Codificar la dirección para la URL
        direccion_codificada = quote(direccion)
        # Usar Nominatim para geocodificar la dirección
        url = f"https://nominatim.openstreetmap.org/search?q={direccion_codificada}&format=json&limit=1"
        headers = {
            'User-Agent': 'EcoGuardian/1.0',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                # Crear el formato geometry de PostGIS
                return f"POINT({lon} {lat})"
            else:
                print(f"No se encontraron resultados para la dirección: {direccion}")
                return None
        else:
            print(f"Error en la respuesta de Nominatim: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error en geocodificación: {str(e)}")
        print(f"Dirección que causó el error: {direccion}")
        return None
 
@vistareportarincendio.route('/reportar_incendio', methods=['GET', 'POST'])
@login_required
def vista_reportarincendio():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            calle_afectada = request.form['calle_afectada']
            severidad = int(request.form['severidad'])  # Convertir a entero
            descripcion = request.form['descripcion']
            fecha_reporte = datetime.now()
            tipo_evento = "Incendio"  # Valor por defecto
            usuario_reporta = current_user.id  # Obtener el ID del usuario actual

            # Geocodificar la dirección
            ubicacion = geocodificar_direccion(calle_afectada)
            if not ubicacion:
                flash('No se pudo encontrar la ubicación exacta de la dirección proporcionada. Por favor, verifica la dirección e intenta nuevamente.', 'error')
                return redirect(url_for('idvistareportarincendio.vista_reportarincendio'))

            # Crear conexión a la base de datos
            conexion = ControlConexion()
            conexion.abrirBd(serv, usua, passw, bdat, port)

            # Insertar el reporte en la base de datos
            sql = """
                INSERT INTO reportes_ambientales 
                (tipo_evento, severidad, descripcion, fecha_reporte, calle_afectada, usuario_reporta, ubicacion)
                VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
            """
            parametros = (tipo_evento, severidad, descripcion, fecha_reporte, calle_afectada, usuario_reporta, ubicacion)
            
            if conexion.ejecutarComandoSql(sql, parametros):
                flash('Reporte de incendio registrado exitosamente', 'success')
                return redirect(url_for('idvistareportarincendio.vista_reportarincendio'))
            else:
                flash('Error al registrar el reporte de incendio', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            if 'conexion' in locals():
                conexion.cerrarBd()

    return render_template('reportar_incendio.html')