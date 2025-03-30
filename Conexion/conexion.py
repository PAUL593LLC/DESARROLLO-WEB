import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="daladier123",  # Asegúrate de no exponer contraseñas en el código fuente en producción
            database="gestion_usuarios"
        )
        if conexion.is_connected():
            # Puedes usar logging en vez de print para producción
            print("Conexión exitosa a la base de datos")
            return conexion
        else:
            print("No se pudo establecer la conexión.")
            return None
    except Error as err:
        print(f"Error al conectar con MySQL: {err}")
        return None

