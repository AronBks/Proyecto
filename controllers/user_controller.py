# user_controller.py
import sys
import os

# Agrega la ruta para acceder a 'views' y 'connector'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from views.connector import DBConnector
from views.usuarioDAO import UsuarioDAO  

class UserController:
    def __init__(self, connector):
        self.connector = connector

    def listar_usuarios(self):
        connection = self.connector.conectar()
        cursor = connection.cursor()
        
        # Recuperar usuarios con campos que coincidan con la estructura de la tabla
        cursor.execute("SELECT id, nombre_apellidos, ci, celular, direccion, correo, estado,id_rol FROM usuarios")
        usuarios = cursor.fetchall()
        
        # Cerrar la conexión
        self.connector.cerrar_conexion(connection)
        
        # Devolver usuarios tal como fueron obtenidos (tuplas)
        return usuarios

    def registrar_usuario(self, nombre_apellidos, ci, celular, direccion, password, correo, estado, id_rol):
        connection = self.connector.conectar()
        cursor = connection.cursor()
        
        # Insertar un nuevo usuario con campos actualizados
        cursor.execute(
            "INSERT INTO usuarios (nombre_apellidos, ci, celular, direccion, password, correo, estado, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nombre_apellidos, ci, celular, direccion, password, correo, estado, id_rol)
        )
        
        # Confirmar cambios
        connection.commit()
        
        # Cerrar la conexión
        self.connector.cerrar_conexion(connection)

    def actualizar_usuario(self, user_id, nombre_apellidos, ci, celular, direccion, correo, password, estado, id_rol):
        connection = self.connector.conectar()
        cursor = connection.cursor()
        
        # Actualizar el usuario con los nuevos campos
        cursor.execute(
            "UPDATE usuarios SET nombre_apellidos = %s, ci = %s, celular = %s, direccion = %s, correo = %s, password = %s, estado = %s, id_rol = %s WHERE id = %s",
            (nombre_apellidos, ci, celular, direccion, correo, password, estado, id_rol, user_id)
        )
        
        # Confirmar cambios
        connection.commit()
        
        # Cerrar la conexión
        self.connector.cerrar_conexion(connection)

    def eliminar_usuario(self, user_id):
        connection = self.connector.conectar()
        cursor = connection.cursor()
        
        # Eliminar el usuario
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        
        # Confirmar cambios
        connection.commit()
        
        # Cerrar la conexión
        self.connector.cerrar_conexion(connection)
