import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="daladier123",
            database="gestion_usuarios"
        )
        print("Conexión exitosa a la base de datos")  # Agregado para depuración
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar con MySQL: {err}")
        return None


