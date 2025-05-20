from flask import Blueprint, render_template, jsonify
import psycopg2
from flask_login import current_user, login_required
from configBd import serv, usua, passw, bdat, port
import ast

vistarutas = Blueprint('vistarutas', __name__)

@vistarutas.route('/rutas')
def panel_rutas():
    return render_template('rutas.html')

@vistarutas.route('/api/rutas_recomendadas')
@login_required
def rutas_recomendadas():
    try:
        id_usuario = current_user.id
        conn = psycopg2.connect(
            dbname=bdat,
            user=usua,
            password=passw,
            host=serv,
            port=port
        )
        cur = conn.cursor()

        # Obtener perfil del usuario
        cur.execute("SELECT perfil_salud FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        result = cur.fetchone()
        perfil_salud_raw = result[0] if result else []

        if isinstance(perfil_salud_raw, str):
            perfiles_usuario = [p.strip().lower() for p in ast.literal_eval(perfil_salud_raw)]
        else:
            perfiles_usuario = [p.lower() for p in perfil_salud_raw] if perfil_salud_raw else []

        restricciones = {
            "asmatico": ["humo", "polen"],
            "alergico al polen": ["polen"],
            "deportista": ["humo", "contaminacion"],
            "sin condicion": []
        }

        eventos_prohibidos = set()
        for perfil in perfiles_usuario:
            eventos_prohibidos.update(restricciones.get(perfil, []))

        cur.execute("SELECT id_ruta, nombre_ruta, coordenadas, calles FROM rutas")
        rutas = cur.fetchall()

        geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        for ruta in rutas:
            id_ruta, nombre_ruta, coordenadas, calles = ruta

            if not isinstance(coordenadas, list):
                continue

            if isinstance(calles, str):
                calles = ast.literal_eval(calles)

            # Filtrar por eventos peligrosos en calles
            if eventos_prohibidos:
                placeholders = ','.join(['%s'] * len(calles))
                cur.execute(f"""
                    SELECT tipo_evento 
                    FROM reportes_ambientales 
                    WHERE LOWER(calle_afectada) IN ({placeholders})
                """, [c.lower() for c in calles])

                eventos_calle = [row[0].lower() for row in cur.fetchall()]
                eventos_peligrosos = [evt for evt in eventos_calle if evt in eventos_prohibidos]

                if eventos_peligrosos:
                    continue  # No mostrar esta ruta

            # Calcular severidad
            cur.execute("""
                SELECT SUM(severidad) 
                FROM reportes_ambientales 
                WHERE LOWER(calle_afectada) = ANY(%s)
            """, ([c.lower() for c in calles],))
            severidad_total = cur.fetchone()[0] or 0

            criticidad = "baja" if severidad_total < 2 else "media" if severidad_total < 4 else "alta"

            geojson["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordenadas
                },
                "properties": {
                    "name": nombre_ruta,
                    "criticidad": criticidad
                }
            })

        cur.close()
        conn.close()
        return jsonify(geojson)

    except Exception as e:
        print(f"❌ Error en el backend: {e}")
        return jsonify({"error": "Error al procesar las rutas"}), 500
