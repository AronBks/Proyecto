import pymysql

class UsuarioDAO:
    def __init__(self, connector):
        self.connector = connector

    def verificar_usuario_existe(self, nombre):
        # Lógica para verificar si el usuario existe en la base de datos
        connection = self.connector.conectar()
        cursor = connection.cursor()
        query = "SELECT * FROM usuarios WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        usuario = cursor.fetchone()
        self.connector.cerrar_conexion(connection)
        return usuario is not None

    def registrar_usuario(self, nombre, contraseña):
        # Lógica para registrar un usuario en la base de datos
        connection = self.connector.conectar()
        cursor = connection.cursor()
        query = "INSERT INTO usuarios (nombre, contraseña) VALUES (%s, %s)"
        cursor.execute(query, (nombre, contraseña))
        connection.commit()
        self.connector.cerrar_conexion(connection)

    def obtener_usuario(self, nombre):
        # Lógica para obtener un usuario de la base de datos
        connection = self.connector.conectar()
        cursor = connection.cursor()
        query = "SELECT * FROM usuarios WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        usuario = cursor.fetchone()
        self.connector.cerrar_conexion(connection)
        return usuario

    def cargar_usuarios(self):
        # Lógica para cargar todos los usuarios
        connection = self.connector.conectar()
        cursor = connection.cursor()
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        usuarios = cursor.fetchall()
        self.connector.cerrar_conexion(connection)
        return usuarios

    def eliminar_usuario(self, id_usuario):
        # Lógica para eliminar un usuario
        connection = self.connector.conectar()
        cursor = connection.cursor()
        query = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(query, (id_usuario,))
        connection.commit()
        self.connector.cerrar_conexion(connection)
