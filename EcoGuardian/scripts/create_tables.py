import os
import sys
from control.ControlConexion import ControlConexion
from configBd import *

def create_tables():
    try:
        # Crear conexión a la base de datos
        conexion = ControlConexion()
        conexion.abrirBd(serv, usua, passw, bdat, port)
        
        # Leer el archivo SQL
        with open('scripts/create_users_table.sql', 'r') as file:
            sql_commands = file.read()
        
        # Ejecutar los comandos SQL
        conexion.ejecutarComandoSql(sql_commands)
        
        print("Tablas creadas exitosamente")
        
    except Exception as e:
        print(f"Error al crear tablas: {str(e)}")
        sys.exit(1)
    finally:
        if 'conexion' in locals():
            conexion.cerrarBd()

if __name__ == '__main__':
    create_tables() 