from flask_login import UserMixin
from Conexion.conexion import obtener_conexion
from werkzeug.security import check_password_hash

class Usuario(UserMixin):
    def __init__(self, id_usuarios, nombre, mail, password):
        self.id = id_usuarios
        self.nombre = nombre
        self.email = mail
        self.password = password

    @staticmethod
    def obtener_por_email(email):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, mail, password FROM usuarios WHERE mail = %s", (email,))
        fila = cursor.fetchone()
        if fila:
            return Usuario(*fila)
        return None

    @staticmethod
    def obtener_por_id(id_usuarios):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, mail, password FROM usuarios WHERE id_usuario = %s", (id_usuarios,))
        fila = cursor.fetchone()
        if fila:
            return Usuario(*fila)
        return None

    def verificar_password(self, password_plano):
        return check_password_hash(self.password, password_plano)
