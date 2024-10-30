import sys
import os

# Asegúrate de que el sistema pueda encontrar el módulo 'views' y 'connector'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from views.connector import DBConnector

class ProductoController:
    def __init__(self, connector):
        self.connector = connector

    def listar_productos(self):
        connection = self.connector.conectar()
        try:
            cursor = connection.cursor()
            # Ejecutar consulta para obtener los productos
            cursor.execute("SELECT id, nombre, descripcion, precio, stock, codigo_barras FROM productos")
            productos = cursor.fetchall()
            return productos
        finally:
            # Cerrar la conexión
            self.connector.cerrar_conexion(connection)

    def registrar_producto(self, codigo_barras, nombre, descripcion, precio, stock):
        connection = self.connector.conectar()
        try:
            cursor = connection.cursor()
            # Ejecutar inserción de nuevo producto
            cursor.execute(
                "INSERT INTO productos (codigo_barras, nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s, %s)",
                (codigo_barras, nombre, descripcion, precio, stock)
            )
            # Confirmar cambios
            connection.commit()
        finally:
            # Cerrar la conexión
            self.connector.cerrar_conexion(connection)

    def actualizar_producto(self, producto_id, codigo_barras, nombre, descripcion, precio, stock):
        connection = self.connector.conectar()
        try:
            cursor = connection.cursor()
            # Ejecutar actualización del producto
            cursor.execute(
                "UPDATE productos SET codigo_barras = %s, nombre = %s, descripcion = %s, precio = %s, stock = %s WHERE id = %s",
                (codigo_barras, nombre, descripcion, precio, stock, producto_id)
            )
            # Confirmar cambios
            connection.commit()
        finally:
            # Cerrar la conexión
            self.connector.cerrar_conexion(connection)

    def eliminar_producto(self, producto_id):
        connection = self.connector.conectar()
        try:
            cursor = connection.cursor()
            # Ejecutar eliminación del producto
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            # Confirmar cambios
            connection.commit()
        finally:
            # Cerrar la conexión
            self.connector.cerrar_conexion(connection)

    def obtener_producto_por_codigo(self, codigo_barras):
        connection = self.connector.conectar()
        try:
            cursor = connection.cursor()
            # Ejecutar consulta para obtener un producto por código de barras
            cursor.execute("SELECT id, nombre, descripcion, precio, stock FROM productos WHERE codigo_barras = %s", (codigo_barras,))
            resultado = cursor.fetchone()
            return resultado
        finally:
            # Cerrar la conexión
            self.connector.cerrar_conexion(connection)
