from flask import request, session, jsonify, Blueprint, redirect, url_for
from configBd import *
from control.ControlConexion import ControlConexion
from flask_login import current_user, login_required
from datetime import datetime

# Crear un Blueprint para las APIs
api = Blueprint('api', __name__)

@api.route('/api/reaccion', methods=['POST'])
@login_required
def api_reaccion():
    if not current_user.is_authenticated:
        return jsonify({
            'status': 'error',
            'message': 'Usuario no autenticado'
        }), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No se recibieron datos'
            }), 400

        id_reporte = data.get('id_reporte')
        tipo_reaccion = data.get('tipo_reaccion')
        comentario = data.get('comentario', '')
        id_usuario = current_user.id

        if not id_reporte:
            return jsonify({
                'status': 'error',
                'message': 'Falta el ID del reporte'
            }), 400

        # Si no hay tipo_reaccion ni comentario, retornar error
        if not tipo_reaccion and not comentario:
            return jsonify({
                'status': 'error',
                'message': 'Debe proporcionar al menos una reacción o un comentario'
            }), 400

        conexion = ControlConexion()
        try:
            conn = conexion.abrirBd(serv, usua, passw, bdat, port)
            
            # Verificar si ya existe una reacción del mismo usuario para este reporte
            sql_check = """
                SELECT id_reaccion, tipo_reaccion, comentario 
                FROM reacciones_reportes 
                WHERE id_reporte = %s AND id_usuario = %s
            """
            resultado = conexion.ejecutarSelect(sql_check, [id_reporte, id_usuario])
            
            if resultado:
                # Actualizar reacción existente
                # Si hay un nuevo comentario, lo agregamos al existente
                comentario_actual = resultado[0]['comentario'] or ''
                if comentario and comentario_actual:
                    comentario_actual += f"\n---\n{comentario}"
                elif comentario:
                    comentario_actual = comentario

                # Mantener el tipo_reaccion existente si no se envía uno nuevo
                tipo_reaccion_actual = resultado[0]['tipo_reaccion']
                if tipo_reaccion and tipo_reaccion != 'neutral':
                    tipo_reaccion_actual = tipo_reaccion

                sql = """
                    UPDATE reacciones_reportes 
                    SET tipo_reaccion = %s,
                        comentario = %s,
                        fecha_reaccion = NOW()
                    WHERE id_reporte = %s AND id_usuario = %s
                """
                parametros = (tipo_reaccion_actual, comentario_actual, id_reporte, id_usuario)
                conexion.ejecutarComandoSql(sql, parametros)
                
                # Obtener el ID de la reacción actualizada
                sql_get_id = """
                    SELECT id_reaccion 
                    FROM reacciones_reportes 
                    WHERE id_reporte = %s AND id_usuario = %s
                """
                id_result = conexion.ejecutarSelect(sql_get_id, [id_reporte, id_usuario])
                id_reaccion = id_result[0]['id_reaccion'] if id_result else None
            else:
                # Insertar nueva reacción
                # Si solo se envía un comentario, establecer tipo_reaccion como neutral
                if not tipo_reaccion:
                    tipo_reaccion = 'neutral'

                sql = """
                    INSERT INTO reacciones_reportes (id_reporte, id_usuario, tipo_reaccion, comentario, fecha_reaccion)
                    VALUES (%s, %s, %s, %s, NOW())
                """
                parametros = (id_reporte, id_usuario, tipo_reaccion, comentario)
                conexion.ejecutarComandoSql(sql, parametros)
                
                # Obtener el ID de la nueva reacción
                sql_get_id = """
                    SELECT id_reaccion 
                    FROM reacciones_reportes 
                    WHERE id_reporte = %s AND id_usuario = %s
                    ORDER BY fecha_reaccion DESC 
                    LIMIT 1
                """
                id_result = conexion.ejecutarSelect(sql_get_id, [id_reporte, id_usuario])
                id_reaccion = id_result[0]['id_reaccion'] if id_result else None
            
            if not id_reaccion:
                raise Exception("No se pudo guardar la reacción")
            
            return jsonify({
                'status': 'ok',
                'message': 'Reacción guardada exitosamente',
                'data': {
                    'id_reaccion': id_reaccion,
                    'id_reporte': id_reporte,
                    'tipo_reaccion': tipo_reaccion_actual if resultado else tipo_reaccion,
                    'comentario': comentario_actual if resultado else comentario
                }
            })
            
        finally:
            conexion.cerrarBd()
            
    except Exception as e:
        print(f"[ERROR] Error al guardar reacción: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error al guardar la reacción: {str(e)}'
        }), 500

@api.route('/api/comentarios/<int:id_reporte>', methods=['GET'])
def obtener_comentarios(id_reporte):
    try:
        conexion = ControlConexion()
        try:
            conn = conexion.abrirBd(serv, usua, passw, bdat, port)
            
            # Obtener todos los comentarios para el reporte
            sql = """
                SELECT r.id_reaccion, r.comentario, r.fecha_reaccion, u.nombre
                FROM reacciones_reportes r
                JOIN usuarios u ON r.id_usuario = u.id_usuario
                WHERE r.id_reporte = %s AND r.comentario IS NOT NULL AND r.comentario != ''
                ORDER BY r.fecha_reaccion DESC
            """
            resultado = conexion.ejecutarSelect(sql, [id_reporte])
            
            comentarios = []
            for row in resultado:
                # Dividir los comentarios si hay múltiples (separados por "---")
                comentarios_texto = row['comentario'].split('---')
                for comentario in comentarios_texto:
                    if comentario.strip():  # Solo agregar comentarios no vacíos
                        comentarios.append({
                            'id_reaccion': row['id_reaccion'],
                            'usuario': row['nombre'],
                            'comentario': comentario.strip(),
                            'fecha': row['fecha_reaccion'].strftime('%d/%m/%Y %H:%M')
                        })
            
            return jsonify({
                'status': 'ok',
                'comentarios': comentarios
            })
            
        finally:
            conexion.cerrarBd()
            
    except Exception as e:
        print(f"[ERROR] Error al obtener comentarios: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener los comentarios: {str(e)}'
        }), 500
